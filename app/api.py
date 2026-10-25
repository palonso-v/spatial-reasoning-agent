import numpy as np
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.agent import (
    LABELS_PATH,
    SCENE_PATH,
    run_agent,
)
from app.scene import load_scene
from app.schemas import (
    AskRequest,
    AskResponse,
    HealthResponse,
    SceneObjectResponse,
    SceneResponse,
)
from app.semantics import (
    apply_labels,
    load_labels,
)
from app.schemas import (
    AskRequest,
    AskResponse,
    HealthResponse,
    SceneObjectPointsResponse,
    SceneObjectResponse,
    ScenePointsResponse,
    SceneResponse,
)


app = FastAPI(
    title="3D Spatial Reasoning Agent",
    description=(
        "Natural-language spatial reasoning "
        "over 3D point-cloud scenes."
    ),
    version="0.4.0",
)

FRONTEND_DIR = Path("frontend")

app.mount(
    "/static",
    StaticFiles(
        directory=FRONTEND_DIR,
    ),
    name="static",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def load_active_scene(
    scene_path: str | Path = SCENE_PATH,
    labels_path: str | Path = LABELS_PATH,
):
    scene = load_scene(
        scene_path
    )

    labels = load_labels(
        labels_path
    )

    return apply_labels(
        scene,
        labels,
    )


@app.get(
    "/health",
    response_model=HealthResponse,
)
def health():
    return {
        "status": "ok",
    }


@app.get(
    "/scene",
    response_model=SceneResponse,
)
def get_scene():
    try:
        scene = load_active_scene()

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc

    objects = [
        SceneObjectResponse(
            object_id=obj.object_id,
            label=obj.label,
            centroid=obj.centroid.tolist(),
            min_bound=obj.min_bound.tolist(),
            max_bound=obj.max_bound.tolist(),
            dimensions=obj.dimensions.tolist(),
            volume=obj.volume,
            point_count=obj.point_count,
        )
        for obj in scene.objects
    ]

    return SceneResponse(
        scene=str(SCENE_PATH),
        object_count=len(objects),
        objects=objects,
    )


@app.post(
    "/ask",
    response_model=AskResponse,
)
def ask(
    request: AskRequest,
):
    try:
        result = run_agent(
            request.question,
            return_trace=True,
            scene_path=SCENE_PATH,
            labels_path=LABELS_PATH,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc

    return AskResponse(
        answer=result["answer"],
        tool_trace=result["tool_trace"],
    )


@app.get(
    "/scene/points",
    response_model=ScenePointsResponse,
)
def get_scene_points():
    try:
        scene = load_active_scene()

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc

    objects = []

    for obj in scene.objects:
        points = np.asarray(
            obj.points
        ).tolist()

        objects.append(
            SceneObjectPointsResponse(
                object_id=obj.object_id,
                label=obj.label,
                points=points,
            )
        )

    return ScenePointsResponse(
        scene=str(SCENE_PATH),
        objects=objects,
    )


@app.get(
    "/",
    include_in_schema=False,
)
def frontend():
    return FileResponse(
        FRONTEND_DIR / "index.html"
    )