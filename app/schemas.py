from typing import Any

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str


class SceneObjectResponse(BaseModel):
    object_id: str
    label: str | None
    centroid: list[float]
    min_bound: list[float]
    max_bound: list[float]
    dimensions: list[float]
    volume: float
    point_count: int


class SceneResponse(BaseModel):
    scene: str
    object_count: int
    objects: list[SceneObjectResponse]


class AskRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=1000,
    )


class ToolTraceItem(BaseModel):
    name: str
    arguments: dict[str, Any]
    result: Any


class AskResponse(BaseModel):
    answer: str
    tool_trace: list[ToolTraceItem]


class SceneObjectPointsResponse(BaseModel):
    object_id: str
    label: str | None
    points: list[list[float]]


class ScenePointsResponse(BaseModel):
    scene: str
    objects: list[SceneObjectPointsResponse]