class OptimizationError(Exception):
    def __init__(self, solver_status: int):
        self.solver_status = solver_status
        super().__init__(f"Optimization failed with status {solver_status}")


class ConstraintError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
