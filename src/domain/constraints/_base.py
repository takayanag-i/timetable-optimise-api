from abc import ABC, abstractmethod
from domain.models.annual_lp_model import AnnualLpModel


class ConstraintApplierBase(ABC):
    @abstractmethod
    def apply(self, model: AnnualLpModel) -> AnnualLpModel:
        raise NotImplementedError()
