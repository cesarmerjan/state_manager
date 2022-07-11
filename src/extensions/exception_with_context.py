from stack_frame_analyzer import StackFrameAnalyzer

stack_frame_analyzer = StackFrameAnalyzer("state_manager")


class ExceptionWithContext(Exception):
    """
    Base class to make exceptions capture the context of whoever raises them.
    """

    def __init__(self, message: str):
        self.message = message
        self.context = stack_frame_analyzer.get_caller_context(depth_in_the_stack=2)
        super().__init__(self.message)

    def __str__(self):
        msg = self.context + "\n"
        msg += f"|-> {self.message}"
        return msg
