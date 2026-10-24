# Spatial Reasoning Agent

An agentic 3D reasoning system that answers natural-language questions about spatial scenes by combining semantic object resolution, deterministic geometry tools, scene-graph reasoning, and LLM tool selection.

The system operates on point-cloud scenes containing segmented objects with semantic labels. The language model interprets the user's request and selects geometry tools, while distances, spatial relationships, containment, and passage constraints are computed deterministically in Python.

The current version focuses on controlled synthetic scenes designed to validate the reasoning architecture before extending the system to real-world 3D perception, spatial memory, SLAM, and richer scene representations.

---

## Features

### 3D Scene Processing

- Point-cloud loading with Open3D
- DBSCAN-based object segmentation
- Axis-aligned bounding-box extraction
- Object centroid calculation
- Object dimension calculation
- Bounding-box volume calculation
- Deterministic object IDs
- Semantic object labels

### Geometry Tools

- Centroid distance between objects
- Surface distance between bounding boxes
- Nearest-object search using centroid distance
- Nearest-object search using physical surface separation
- Relative spatial position:
  - left / right
  - in front / behind
  - above / below
- Bounding-box overlap detection
- Radius-based object search
- Largest-object detection
- Object containment checks
- Passage-through-opening checks

### Scene Graph

- Structured spatial relationships between scene objects
- Bidirectional directional relations
- `NEAR` relations based on surface separation
- `OVERLAPS` relationships
- Semantic relation queries
- Multi-relation reasoning

Current relation types include:

```text
LEFT_OF
RIGHT_OF
IN_FRONT_OF
BEHIND
ABOVE
BELOW
NEAR
OVERLAPS
```

### Semantic Reasoning

- Semantic labels such as `table`, `box`, `chair`, and `cabinet`
- Natural-language label normalization
- Mapping semantic names to internal object IDs
- Semantic labels returned alongside object IDs
- Scene-graph relations enriched with semantic labels

### Agentic Workflow

- OpenAI Responses API tool calling
- Dynamic geometry-tool selection
- Multi-step tool execution
- Semantic object resolution before geometry operations
- Composition of multiple spatial relations
- Tool-result grounding
- Explicit distinction between centroid distance and physical surface distance
- Explicit distinction between containment and passage through an opening
- Maximum-step termination guard
- Tool failure handling

---

## Technology Stack

Python, OpenAI API, Open3D, NumPy, Pydantic, python-dotenv, and pytest.

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/palonso-v/spatial-reasoning-agent.git
cd spatial-reasoning-agent
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the repository root:

```text
OPENAI_API_KEY=your_openai_api_key
```

An OpenAI API account with available API credits is required for agent execution and evaluation.

---

## Generate the Demo Scene

The repository includes a synthetic scene used for development and evaluation.

Generate it with:

```bash
python -m scripts.generate_demo_scene
```

The generated point cloud is stored at:

```text
data/demo_scene.ply
```

Semantic labels are stored in:

```text
data/demo_labels.json
```

The current scene contains five semantic objects:

```text
table
box
chair
cabinet
doorway_opening
```

---

## Inspect the Scene

Run:

```bash
python -m scripts.test_scene
```

The script prints detected objects together with:

- object ID
- semantic label
- centroid
- dimensions
- bounding-box volume
- point count

Example object representation:

```text
object_id: object_1
label: box
dimensions: [0.6, 0.6, 0.6]
volume: 0.216
```

---

## Inspect the Scene Graph

Run:

```bash
python -m scripts.test_scene_graph
```

The scene graph contains directional and proximity relationships between objects.

Example:

```text
table LEFT_OF box
table IN_FRONT_OF box
table ABOVE box
table NEAR box
```

Each directional relationship is also represented in the inverse direction.

For example:

```text
table LEFT_OF box
box RIGHT_OF table
```

---

## Run the Agent

Run:

```bash
python -m app.agent
```

Example question:

```text
Which object is both near the table and in front of it?
```

A typical execution is:

```text
find_object_by_label("table")
        |
        v
object_0
        |
        v
find_objects_by_relation(object_0, "NEAR")
        |
        v
box
        |
        +
        |
find_objects_by_relation(object_0, "IN_FRONT_OF")
        |
        v
box
        |
        v
Final Answer
```

Example final answer:

```text
The box is both near and in front of the table.
```

---

## Example Spatial Queries

### Relative Position

```text
Is the box left of the chair?
```

The agent resolves the semantic labels and uses the `relative_position` geometry tool.

Example result:

```text
Yes, the box is left of the chair.
```

### Physical Proximity

```text
Which object is physically closest to the table?
```

The agent uses physical bounding-box separation rather than centroid distance.

Example:

```text
box
surface distance = 0.4 units
```

### Centroid Distance

```text
Which object is closest to the table by center distance?
```

The agent uses centroid distance instead.

Example:

```text
box
centroid distance ≈ 1.483 units
```

### Containment

```text
Can the box fit inside the cabinet?
```

The agent uses:

```text
can_fit_inside
```

The tool compares object dimensions while allowing axis reordering.

Example:

```text
box:
0.6 × 0.6 × 0.6

cabinet:
0.7 × 1.2 × 1.8

fits = True
```

### Passage Through an Opening

```text
Can the box pass through the doorway opening?
```

The agent uses:

```text
can_pass_through_opening
```

rather than the general containment tool.

The passage calculation compares the object's cross-section with the usable opening dimensions.

Example:

```text
box cross-section:
0.6 × 0.6

doorway opening:
1.0 × 2.1

fits = True
```

This distinction prevents doorway thickness from being incorrectly treated as a limiting passage dimension.

---

## Spatial Reasoning Architecture

```text
Natural-Language Question
          |
          v
      LLM Agent
          |
          v
Semantic Object Resolution
          |
          v
 +---------------------------+
 |                           |
 v                           v
Geometry Tools           Scene Graph
 |                           |
 +-------------+-------------+
               |
               v
       Deterministic Results
               |
               v
      Grounded Final Answer
```

The LLM does not estimate geometric quantities directly.

Its responsibilities are:

- interpret the user request
- identify relevant objects
- choose the appropriate geometry tools
- combine intermediate tool results
- generate the final answer

Geometry remains implemented deterministically in Python.

---

## Geometry Layer

The geometry layer currently operates primarily on axis-aligned bounding boxes.

For each object, the scene representation contains:

```text
object ID
semantic label
centroid
minimum bound
maximum bound
dimensions
point count
volume
```

Example:

```text
SceneObject
 |
 +-- object_id
 +-- label
 +-- centroid
 +-- min_bound
 +-- max_bound
 +-- dimensions
 +-- point_count
 +-- volume
```

---

## Scene Graph Architecture

```text
3D Scene
   |
   v
Segmented Objects
   |
   v
Centroids + Bounding Boxes
   |
   v
Pairwise Spatial Analysis
   |
   +---------------------+
   |                     |
   v                     v
Directional Relations   Surface Distance
   |                     |
   v                     v
LEFT / RIGHT             NEAR
FRONT / BEHIND
ABOVE / BELOW
   |
   +----------+----------+
              |
              v
          Scene Graph
```

The graph provides a structured representation that can be queried without recomputing every spatial relationship during each agent request.

---

## Semantic Layer

Semantic labels are currently supplied through:

```text
data/demo_labels.json
```

Example:

```json
{
  "object_0": "table",
  "object_1": "box",
  "object_2": "chair",
  "object_3": "cabinet",
  "object_4": "doorway_opening"
}
```

Natural-language labels are normalized before lookup.

For example:

```text
doorway opening
```

can resolve to:

```text
doorway_opening
```

The current semantic layer is intentionally simple.

Future versions can replace manually supplied labels with learned 3D semantic segmentation or open-vocabulary scene understanding.

---

## Evaluation

The repository includes a controlled spatial-reasoning benchmark containing:

```text
20 questions
```

The benchmark evaluates:

- semantic object resolution
- geometry-tool selection
- centroid-distance reasoning
- surface-distance reasoning
- directional relationships
- `NEAR` relationships
- multi-relation reasoning
- object containment
- doorway passage
- overlap detection
- radius queries
- largest-object queries

Run:

```bash
python -m evals.run_agent_eval
```

Current baseline:

```text
Overall: 20/20
Tool selection: 20/20
Answer checks: 20/20
Average tool calls: 2.65
```

The evaluation also verifies expected tool sequences.

Example:

```text
Question:
Can the box pass through the doorway opening?

Expected tools:
find_object_by_label
find_object_by_label
can_pass_through_opening
```

---

## Evaluation Scope

The current benchmark uses:

- one synthetic scene
- five semantic objects
- hand-designed spatial questions
- deterministic geometry
- LLM-based tool selection and answer generation

The current 100% result should therefore be interpreted as a regression baseline for the current controlled environment.

It does not establish general 3D spatial-reasoning accuracy.

Future evaluations will require:

- paraphrased questions
- multiple scene layouts
- larger object sets
- ambiguous queries
- noisy point clouds
- real reconstructed scenes
- learned semantic labels

---

## Project Structure

```text
spatial-reasoning-agent/
├── app/
│   ├── __init__.py
│   ├── agent.py
│   ├── scene.py
│   ├── scene_graph.py
│   ├── semantics.py
│   └── tools/
│       ├── __init__.py
│       └── geometry.py
│
├── data/
│   ├── demo_labels.json
│   └── demo_scene.ply
│
├── evals/
│   ├── __init__.py
│   ├── run_agent_eval.py
│   └── spatial_cases.py
│
├── scripts/
│   ├── generate_demo_scene.py
│   ├── test_scene.py
│   └── test_scene_graph.py
│
├── requirements.txt
└── README.md
```

---

## Design Principles

### Deterministic Geometry

The LLM is not used to estimate distances, dimensions, overlap, or containment.

These operations are performed by deterministic geometry functions.

```text
LLM
 |
 v
Select Tool
 |
 v
Geometry Function
 |
 v
Computed Result
```

This reduces hallucination risk for numerical and spatial quantities.

### Explicit Tool Semantics

Different geometric concepts are handled by separate tools.

For example:

```text
find_nearest_object
-> centroid distance

find_nearest_object_by_surface
-> physical surface separation

can_fit_inside
-> volumetric containment

can_pass_through_opening
-> passage clearance
```

The distinction prevents geometrically different questions from being collapsed into the same operation.

### Semantic Labels Alongside Object IDs

Internal object identifiers such as:

```text
object_1
```

are useful for deterministic processing but are not meaningful to users.

Geometry tools that discover objects therefore return both:

```text
object_id
label
```

Example:

```json
{
  "object_id": "object_1",
  "label": "box"
}
```

This reduces unnecessary follow-up tool calls and improves answer readability.

### Structured Scene Representation

Spatial relationships are precomputed into a scene graph.

The agent can query relationships such as:

```text
NEAR(table)
```

or:

```text
IN_FRONT_OF(table)
```

and combine their results.

### Evaluation Before Added Complexity

The current implementation deliberately uses a simple tool-calling loop rather than a larger orchestration framework.

More complex orchestration will be introduced only when evaluation shows a concrete need for:

- explicit planning
- verification
- persistent state
- richer execution control

---

## Limitations

This project is currently an early-stage research and portfolio prototype.

Current limitations include:

- evaluation uses a single synthetic scene
- semantic labels are manually provided
- segmentation uses DBSCAN rather than learned instance segmentation
- object geometry is represented using axis-aligned bounding boxes
- object orientation is not modeled explicitly
- containment reasoning uses bounding-box dimensions
- doorway passage assumes a known passage axis
- the scene does not yet include realistic walls, floors, or reconstructed environments
- the agent currently uses a simple OpenAI tool-calling loop
- no graphical 3D interface is implemented yet
- real-world point-cloud noise has not yet been evaluated
- SLAM and spatial memory are not yet implemented
- Gaussian Splatting is not yet integrated

---

## Future Improvements

Planned extensions include:

- paraphrase and robustness evaluation
- multi-scene evaluation
- more realistic synthetic environments
- real-world point-cloud ingestion
- learned semantic segmentation
- object orientation and oriented bounding boxes
- richer scene graphs
- FastAPI backend
- interactive 3D visualization
- object highlighting and measurement visualization
- explicit planning and verification
- LangGraph orchestration where useful
- spatial memory
- SLAM integration
- Gaussian Splatting support
- richer 3D scene representations
- embodied-agent style spatial tasks

---

## Long-Term Direction

The long-term goal is to develop the system from a static geometry agent into a broader spatial AI agent.

Potential progression:

```text
Geometry Agent
      |
      v
Semantic Scene Understanding
      |
      v
Scene Graph Reasoning
      |
      v
Spatial Memory
      |
      v
SLAM / Dynamic Mapping
      |
      v
Rich 3D Representations
      |
      v
Embodied Spatial Agent
```

The central design principle remains the same:

```text
LLM -> reasoning and tool selection

3D system -> perception, geometry, and spatial computation
```

---

## Author

Pedro Alonso Vaquero

[GitHub](https://github.com/palonso-v)