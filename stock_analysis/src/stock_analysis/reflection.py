from inspect import cleandoc
from functools import cache
from typing import Optional, List, Any
from pydantic import Field
from pydantic import BaseModel
from crewai import Task
from crewai.tasks.task_output import TaskOutput
from crewai.agent import BaseAgent

class Feedback(BaseModel):
    feedback: str
    score: int 

class ReflectionTask(Task):

    reflection_agent: BaseAgent = Field(
        description="Agent responsible for reflecting on the task."
    )

    reflection_task: Task = Field(description="Task to be executed by the reflection agent.", default=None)

    @cache
    def _create_reflection_task(self) -> Task:
        return Task(
            description=cleandoc(
                """Create actionable and constructive feedback for the result of the previous task.
                Also give a 0 - 3 score evaluating the result of the previous task (0 being the lowest quality response and 3 being the best possible response).
                """),
            expected_output="A json with a 'feedback' field describing how the quality of the task output can be improved and a 'score' field.",
            output_json=Feedback,
        )

    def _execute_core(
        self,
        agent: Optional[BaseAgent],
        context: Optional[str],
        tools: Optional[List[Any]],
        max_iter: int = 5
    ) -> TaskOutput:
        """Run the core execution logic of the task."""
        self.description: str
        agent = agent or self.agent
        self.agent = agent
        if not agent:
            raise Exception(
                f"The task '{self.description}' has no agent assigned, therefore it can't be executed directly and should be executed in a Crew using a specific process that support that, like hierarchical."
            )
        reflection_agent = self.reflection_agent or agent
        if not reflection_agent:
            raise Exception(
                f"The task '{self.description}' has no reflection agent assigned."
            )
        reflection_task = self.reflection_task or self._create_reflection_task()

        start_time = self._set_start_execution_time()
        self._execution_span = self._telemetry.task_started(crew=agent.crew, task=self)

        self.prompt_context = context
        tools = tools or self.tools or []

        self.processed_by_agents.add(agent.role)

        original_description: str = self.description
        for i in range(max_iter):
            if i > 0:
                reflection_result = reflection_agent.execute_task(
                    reflection_task, 
                    context=context, 
                    tools=tools
                )
                _, reflection_json_output = self._export_output(reflection_result)
                print(reflection_json_output)
                self.description = original_description
                if reflection_json_output:
                    if "score" in reflection_json_output and reflection_json_output['score'] == 3:
                        break
                    if "feedback" in reflection_json_output:
                        self.description += f"\nPlease incorporate the following feedback if present: {reflection_json_output['feedback']}"
                    
            
            result = agent.execute_task(
                task=self,
                context=context,
                tools=tools,
            )

        self.description = original_description
        pydantic_output, json_output = self._export_output(result)

        task_output = TaskOutput(
            name=self.name,
            description=self.description,
            expected_output=self.expected_output,
            raw=result,
            pydantic=pydantic_output,
            json_dict=json_output,
            agent=agent.role,
            output_format=self._get_output_format(),
        )
        self.output = task_output

        self._set_end_execution_time(start_time)
        if self.callback:
            self.callback(self.output)

        if self._execution_span:
            self._telemetry.task_ended(self._execution_span, self, agent.crew)
            self._execution_span = None

        if self.output_file:
            content = (
                json_output
                if json_output
                else pydantic_output.model_dump_json() if pydantic_output else result
            )
            self._save_file(content)

        return task_output


