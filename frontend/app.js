import * as THREE from "three";

import {
    OrbitControls
} from "three/addons/controls/OrbitControls.js";


const API_BASE = "";


const OBJECT_COLORS = {
    table: 0xd59a4a,
    stool: 0xe84a5f,
    chair: 0x4a90e2,
    cabinet: 0x55b86a,
    doorway_opening: 0xb0b0b0,
};

const viewer =
    document.getElementById(
        "viewer"
    );

const statusElement =
    document.getElementById(
        "status"
    );

const objectListElement =
    document.getElementById(
        "object-list"
    );

const questionInput =
    document.getElementById(
        "question-input"
    );

const askButton =
    document.getElementById(
        "ask-button"
    );

const answerText =
    document.getElementById(
        "answer-text"
    );

const traceText =
    document.getElementById(
        "trace-text"
    );


const scene =
    new THREE.Scene();

scene.background =
    new THREE.Color(
        0x0b1120
    );


const camera =
    new THREE.PerspectiveCamera(
        60,
        viewer.clientWidth /
            viewer.clientHeight,
        0.01,
        1000
    );


const renderer =
    new THREE.WebGLRenderer({
        antialias: true,
    });

renderer.setPixelRatio(
    window.devicePixelRatio
);

renderer.setSize(
    viewer.clientWidth,
    viewer.clientHeight
);

viewer.appendChild(
    renderer.domElement
);


const controls =
    new OrbitControls(
        camera,
        renderer.domElement
    );

controls.enableDamping = true;

controls.dampingFactor =
    0.08;


const grid =
    new THREE.GridHelper(
        12,
        24,
        0x374151,
        0x1f2937
    );

grid.rotation.x =
    Math.PI / 2;

scene.add(
    grid
);


const axes =
    new THREE.AxesHelper(
        1.5
    );

scene.add(
    axes
);


const pointCloudObjects =
    new Map();

const sidebarItems =
    new Map();

const sceneMetadata =
    new Map();

const visualHelpers =
    [];

const reasoningSteps =
    document.getElementById(
        "reasoning-steps"
    );

function getColor(
    label
) {

    return (
        OBJECT_COLORS[label]
        ?? 0xffffff
    );
}


function addObjectToScene(
    object
) {

    const positions =
        new Float32Array(
            object.points.length * 3
        );


    object.points.forEach(
        (
            point,
            index
        ) => {

            positions[
                index * 3
            ] = point[0];

            positions[
                index * 3 + 1
            ] = point[1];

            positions[
                index * 3 + 2
            ] = point[2];
        }
    );


    const geometry =
        new THREE.BufferGeometry();


    geometry.setAttribute(
        "position",
        new THREE.BufferAttribute(
            positions,
            3
        )
    );


    geometry.computeBoundingBox();


    const color =
        getColor(
            object.label
        );


    const material =
        new THREE.PointsMaterial({
            color: color,
            size: 0.07,
            sizeAttenuation: true,
        });


    const points =
        new THREE.Points(
            geometry,
            material
        );


    points.userData = {
        objectId:
            object.object_id,

        label:
            object.label,
    };


    scene.add(
        points
    );


    pointCloudObjects.set(
        object.object_id,
        points
    );


    const box =
        geometry.boundingBox;


    if (
        box
    ) {

        const center =
            box.getCenter(
                new THREE.Vector3()
            );

        const size =
            box.getSize(
                new THREE.Vector3()
            );


        sceneMetadata.set(
            object.object_id,
            {
                center: center,
                size: size,
            }
        );
    }


    addObjectToSidebar(
        object,
        color
    );
}


function addObjectToSidebar(
    object,
    color
) {

    const item =
        document.createElement(
            "div"
        );

    item.className =
        "object-item";


    const indicator =
        document.createElement(
            "div"
        );

    indicator.className =
        "color-indicator";

    indicator.style.background =
        `#${color
            .toString(16)
            .padStart(6, "0")}`;


    const textContainer =
        document.createElement(
            "div"
        );


    const label =
        document.createElement(
            "div"
        );

    label.className =
        "object-label";

    label.textContent =
        object.label
        ?? "unknown";


    const id =
        document.createElement(
            "div"
        );

    id.className =
        "object-id";

    id.textContent =
        object.object_id;


    textContainer.appendChild(
        label
    );

    textContainer.appendChild(
        id
    );


    item.appendChild(
        indicator
    );

    item.appendChild(
        textContainer
    );


    objectListElement.appendChild(
        item
    );


    sidebarItems.set(
        object.object_id,
        item
    );


    item.addEventListener(
        "click",
        () => {

            clearHighlights();

            highlightObject(
                object.object_id
            );
        }
    );
}


function clearVisualHelpers() {

    for (
        const helper
        of visualHelpers
    ) {

        scene.remove(
            helper
        );

        if (
            helper.geometry
        ) {

            helper.geometry.dispose();
        }

        if (
            helper.material
        ) {

            helper.material.dispose();
        }
    }


    visualHelpers.length = 0;
}


function clearHighlights() {

    pointCloudObjects.forEach(
        (
            points
        ) => {

            const label =
                points.userData.label;


            points.material.color.setHex(
                getColor(
                    label
                )
            );

            points.material.size =
                0.07;
        }
    );


    sidebarItems.forEach(
        (
            item
        ) => {

            item.classList.remove(
                "highlighted"
            );
        }
    );


    clearVisualHelpers();
}


function addBoundingBox(
    objectId
) {

    const points =
        pointCloudObjects.get(
            objectId
        );


    if (
        !points
    ) {
        return;
    }


    const helper =
        new THREE.BoxHelper(
            points,
            0xfacc15
        );


    scene.add(
        helper
    );


    visualHelpers.push(
        helper
    );
}


function highlightObject(
    objectId
) {

    const points =
        pointCloudObjects.get(
            objectId
        );


    if (
        !points
    ) {
        return;
    }


    points.material.color.setHex(
        0xfacc15
    );

    points.material.size =
        0.11;


    addBoundingBox(
        objectId
    );


    const sidebarItem =
        sidebarItems.get(
            objectId
        );


    if (
        sidebarItem
    ) {

        sidebarItem.classList.add(
            "highlighted"
        );
    }
}


function extractObjectIds(
    toolTrace
) {

    const objectIds =
        new Set();


    function scanValue(
        value
    ) {

        if (
            typeof value === "string"
            &&
            value.startsWith(
                "object_"
            )
        ) {

            objectIds.add(
                value
            );

            return;
        }


        if (
            Array.isArray(
                value
            )
        ) {

            value.forEach(
                scanValue
            );

            return;
        }


        if (
            value
            &&
            typeof value === "object"
        ) {

            Object.values(
                value
            ).forEach(
                scanValue
            );
        }
    }


    for (
        const item
        of toolTrace
    ) {

        scanValue(
            item.arguments
        );

        scanValue(
            item.result
        );
    }


    return [
        ...objectIds
    ];
}


function drawCentroidLine(
    objectA,
    objectB
) {

    const metaA =
        sceneMetadata.get(
            objectA
        );

    const metaB =
        sceneMetadata.get(
            objectB
        );


    if (
        !metaA
        ||
        !metaB
    ) {
        return;
    }


    const geometry =
        new THREE.BufferGeometry()
            .setFromPoints(
                [
                    metaA.center,
                    metaB.center,
                ]
            );


    const material =
        new THREE.LineBasicMaterial({
            color:
                0x22d3ee,
        });


    const line =
        new THREE.Line(
            geometry,
            material
        );


    scene.add(
        line
    );


    visualHelpers.push(
        line
    );


    addCentroidMarker(
        metaA.center
    );

    addCentroidMarker(
        metaB.center
    );
}


function closestPointBetweenBoxes(
    boxA,
    boxB
) {

    const pointA =
        new THREE.Vector3();

    const pointB =
        new THREE.Vector3();


    for (
        const axis
        of ["x", "y", "z"]
    ) {

        if (
            boxA.max[axis]
            <
            boxB.min[axis]
        ) {

            pointA[axis] =
                boxA.max[axis];

            pointB[axis] =
                boxB.min[axis];

        } else if (
            boxB.max[axis]
            <
            boxA.min[axis]
        ) {

            pointA[axis] =
                boxA.min[axis];

            pointB[axis] =
                boxB.max[axis];

        } else {

            const overlapMin =
                Math.max(
                    boxA.min[axis],
                    boxB.min[axis]
                );

            const overlapMax =
                Math.min(
                    boxA.max[axis],
                    boxB.max[axis]
                );

            const midpoint =
                (
                    overlapMin
                    +
                    overlapMax
                ) / 2;

            pointA[axis] =
                midpoint;

            pointB[axis] =
                midpoint;
        }
    }


    return {
        pointA,
        pointB,
    };
}


function drawSurfaceDistanceLine(
    objectA,
    objectB
) {

    const pointsA =
        pointCloudObjects.get(
            objectA
        );

    const pointsB =
        pointCloudObjects.get(
            objectB
        );


    if (
        !pointsA
        ||
        !pointsB
    ) {
        return;
    }


    const boxA =
        pointsA.geometry
            .boundingBox;

    const boxB =
        pointsB.geometry
            .boundingBox;


    if (
        !boxA
        ||
        !boxB
    ) {
        return;
    }


    const {
        pointA,
        pointB,
    } =
        closestPointBetweenBoxes(
            boxA,
            boxB
        );


    const geometry =
        new THREE.BufferGeometry()
            .setFromPoints(
                [
                    pointA,
                    pointB,
                ]
            );


    const material =
        new THREE.LineBasicMaterial({
            color:
                0xf472b6,
        });


    const line =
        new THREE.Line(
            geometry,
            material
        );


    scene.add(
        line
    );


    visualHelpers.push(
        line
    );


    addSurfaceMarker(
        pointA
    );

    addSurfaceMarker(
        pointB
    );
}


function addSurfaceMarker(
    position
) {

    const geometry =
        new THREE.SphereGeometry(
            0.08,
            16,
            16
        );


    const material =
        new THREE.MeshBasicMaterial({
            color:
                0xf472b6,
        });


    const sphere =
        new THREE.Mesh(
            geometry,
            material
        );


    sphere.position.copy(
        position
    );


    scene.add(
        sphere
    );


    visualHelpers.push(
        sphere
    );
}


function createCrossSectionRectangle(
    center,
    width,
    height,
    color,
    yOffset = 0
) {

    const halfWidth =
        width / 2;

    const halfHeight =
        height / 2;


    const y =
        center.y
        +
        yOffset;


    const vertices = [
        new THREE.Vector3(
            center.x - halfWidth,
            y,
            center.z - halfHeight
        ),

        new THREE.Vector3(
            center.x + halfWidth,
            y,
            center.z - halfHeight
        ),

        new THREE.Vector3(
            center.x + halfWidth,
            y,
            center.z + halfHeight
        ),

        new THREE.Vector3(
            center.x - halfWidth,
            y,
            center.z + halfHeight
        ),
    ];


    const points = [
        vertices[0],
        vertices[1],

        vertices[1],
        vertices[2],

        vertices[2],
        vertices[3],

        vertices[3],
        vertices[0],
    ];


    const geometry =
        new THREE.BufferGeometry()
            .setFromPoints(
                points
            );


    const material =
        new THREE.LineBasicMaterial({
            color: color,
        });


    const rectangle =
        new THREE.LineSegments(
            geometry,
            material
        );


    scene.add(
        rectangle
    );


    visualHelpers.push(
        rectangle
    );


    return rectangle;
}


function drawDoorwayClearance(
    objectId,
    openingId,
    result
) {

    const openingMeta =
        sceneMetadata.get(
            openingId
        );


    if (
        !openingMeta
        ||
        !result
    ) {
        return;
    }


    const openingCrossSection =
        result.opening_cross_section;

    const objectCrossSection =
        result.object_cross_section;


    if (
        !openingCrossSection
        ||
        !objectCrossSection
    ) {
        return;
    }


    const openingWidth =
        openingCrossSection[0];

    const openingHeight =
        openingCrossSection[1];


    const objectWidth =
        objectCrossSection[0];

    const objectHeight =
        objectCrossSection[1];


    /*
     * Cyan:
     * actual available doorway cross-section.
     */
    createCrossSectionRectangle(
        openingMeta.center,
        openingWidth,
        openingHeight,
        0x22d3ee,
        0
    );


    /*
     * Magenta:
     * cross-section required by the object.
     *
     * A tiny Y offset prevents both rectangles
     * from occupying exactly the same plane.
     */
    createCrossSectionRectangle(
        openingMeta.center,
        objectWidth,
        objectHeight,
        0xf472b6,
        -0.015
    );


    addDoorwayCenterMarker(
        openingMeta.center,
        result.fits
    );
}


function addDoorwayCenterMarker(
    position,
    fits
) {

    const geometry =
        new THREE.SphereGeometry(
            0.07,
            16,
            16
        );


    const material =
        new THREE.MeshBasicMaterial({
            color:
                fits
                ? 0x22c55e
                : 0xef4444,
        });


    const sphere =
        new THREE.Mesh(
            geometry,
            material
        );


    sphere.position.copy(
        position
    );


    scene.add(
        sphere
    );


    visualHelpers.push(
        sphere
    );
}


function addCentroidMarker(
    position
) {

    const geometry =
        new THREE.SphereGeometry(
            0.09,
            16,
            16
        );


    const material =
        new THREE.MeshBasicMaterial({
            color:
                0x22d3ee,
        });


    const sphere =
        new THREE.Mesh(
            geometry,
            material
        );


    sphere.position.copy(
        position
    );


    scene.add(
        sphere
    );


    visualHelpers.push(
        sphere
    );
}


function visualizeToolTrace(
    toolTrace
) {

    const objectIds =
        extractObjectIds(
            toolTrace
        );


    objectIds.forEach(
        (
            objectId
        ) => {

            highlightObject(
                objectId
            );
        }
    );


    for (
        const item
        of toolTrace
    ) {

        if (
            item.name ===
            "distance_between_objects"
        ) {

            drawCentroidLine(
                item.arguments.object_a,
                item.arguments.object_b
            );
        }


        if (
            item.name ===
            "surface_distance_between_objects"
        ) {

            drawSurfaceDistanceLine(
                item.arguments.object_a,
                item.arguments.object_b
            );
        }


        if (
            item.name ===
            "can_pass_through_opening"
        ) {

            drawDoorwayClearance(
                item.arguments.object_id,
                item.arguments.opening_id,
                item.result
            );
        }
    }
}


function fitCameraToScene() {

    const boundingBox =
        new THREE.Box3();


    pointCloudObjects.forEach(
        (
            points
        ) => {

            points.geometry
                .computeBoundingBox();


            const box =
                points.geometry
                    .boundingBox;


            if (
                box
            ) {

                boundingBox.union(
                    box
                );
            }
        }
    );


    if (
        boundingBox.isEmpty()
    ) {
        return;
    }


    const center =
        boundingBox.getCenter(
            new THREE.Vector3()
        );


    const size =
        boundingBox.getSize(
            new THREE.Vector3()
        );


    const maxDimension =
        Math.max(
            size.x,
            size.y,
            size.z
        );


    camera.position.set(
        center.x +
            maxDimension * 0.7,

        center.y -
            maxDimension * 1.2,

        center.z +
            maxDimension * 0.8
    );


    controls.target.copy(
        center
    );


    camera.lookAt(
        center
    );


    controls.update();
}


async function loadScene() {

    try {

        const response =
            await fetch(
                `${API_BASE}/scene/points`
            );


        if (
            !response.ok
        ) {

            throw new Error(
                `HTTP ${response.status}`
            );
        }


        const data =
            await response.json();


        data.objects.forEach(
            addObjectToScene
        );


        fitCameraToScene();


        const totalPoints =
            data.objects.reduce(
                (
                    total,
                    object
                ) =>
                    total +
                    object.points.length,
                0
            );


        statusElement.textContent =
            `${data.objects.length} objects · ` +
            `${totalPoints} points`;

    } catch (
        error
    ) {

        console.error(
            error
        );


        statusElement.textContent =
            "Failed to load scene";
    }
}


async function askQuestion() {

    const question =
        questionInput.value.trim();


    if (
        !question
    ) {
        return;
    }


    clearHighlights();


    askButton.disabled =
        true;

    askButton.textContent =
        "Thinking...";


    answerText.textContent =
        "Processing question...";


    traceText.textContent =
        "";

    reasoningSteps.textContent =
        "Processing reasoning steps...";


    try {

        const response =
            await fetch(
                `${API_BASE}/ask`,
                {
                    method:
                        "POST",

                    headers: {
                        "Content-Type":
                            "application/json",
                    },

                    body:
                        JSON.stringify(
                            {
                                question:
                                    question,
                            }
                        ),
                }
            );


        if (
            !response.ok
        ) {

            throw new Error(
                `HTTP ${response.status}`
            );
        }


        const data =
            await response.json();


        answerText.textContent =
            data.answer;


        traceText.textContent =
            JSON.stringify(
                data.tool_trace,
                null,
                2
            );

        renderReasoningSteps(
            data.tool_trace
        );

        visualizeToolTrace(
            data.tool_trace
        );

    } catch (
        error
    ) {

        console.error(
            error
        );


        answerText.textContent =
            "Failed to get an answer.";

    } finally {

        askButton.disabled =
            false;

        askButton.textContent =
            "Ask";
    }
}


function animate() {

    requestAnimationFrame(
        animate
    );


    controls.update();


    renderer.render(
        scene,
        camera
    );
}


function describeToolStep(
    item
) {

    const args =
        item.arguments ?? {};

    const result =
        item.result ?? {};


    switch (
        item.name
    ) {

        case "find_object_by_label":
            return (
                `Resolved "${args.label}" ` +
                `to ${result.label ?? result.object_id}.`
            );


        case "find_largest_object":
            return (
                `Compared object bounding-box volumes ` +
                `and found ${result.label ?? result.object_id} ` +
                `to be the largest.`
            );


        case "find_nearest_object":
            return (
                `Compared centroid distances from ` +
                `${args.reference_object} and found ` +
                `${result.label ?? result.object_id} nearest.`
            );


        case "find_nearest_object_by_surface":
            return (
                `Compared physical surface separation from ` +
                `${args.reference_object} and found ` +
                `${result.label ?? result.object_id} nearest.`
            );


        case "distance_between_objects":
            return (
                `Computed centroid distance between ` +
                `${args.object_a} and ${args.object_b}: ` +
                `${Number(result.distance).toFixed(3)} units.`
            );


        case "surface_distance_between_objects":
            return (
                `Computed the minimum bounding-box surface ` +
                `separation between ${args.object_a} and ` +
                `${args.object_b}: ` +
                `${Number(result.surface_distance).toFixed(3)} units.`
            );


        case "relative_position":
            return (
                `Compared the positions of ` +
                `${args.object_a} and ${args.object_b}: ` +
                `${(result.relations ?? []).join(", ")}.`
            );


        case "bounding_boxes_overlap":
            return (
                `Checked whether the bounding boxes of ` +
                `${args.object_a} and ${args.object_b} overlap: ` +
                `${result.overlap ? "yes" : "no"}.`
            );


        case "objects_within_radius":
            return (
                `Searched for objects within ` +
                `${args.radius} units of ` +
                `${args.reference_object}.`
            );


        case "can_fit_inside":
            return (
                `Compared object and container dimensions: ` +
                `${result.fits ? "the object fits" : "the object does not fit"}.`
            );


        case "can_pass_through_opening":
            return (
                `Compared the object's required cross-section ` +
                `with the opening: ` +
                `${result.fits ? "passage is possible" : "passage is blocked"}.`
            );


        case "find_objects_by_relation":
            return (
                `Queried the scene graph for objects ` +
                `${args.relation} ${args.reference_object}.`
            );


        case "describe_object_relations":
            return (
                `Retrieved the scene-graph relationships ` +
                `for ${args.object_id}.`
            );


        case "scene_summary":
            return (
                "Inspected the detected objects and scene geometry."
            );


        default:
            return (
                `Used ${item.name}.`
            );
    }
}


function renderReasoningSteps(
    toolTrace
) {

    reasoningSteps.innerHTML =
        "";


    if (
        !toolTrace
        ||
        toolTrace.length === 0
    ) {

        reasoningSteps.textContent =
            "No geometry tools were required.";

        return;
    }


    toolTrace.forEach(
        (
            item,
            index
        ) => {

            const step =
                document.createElement(
                    "div"
                );

            step.className =
                "reasoning-step";


            const number =
                document.createElement(
                    "span"
                );

            number.className =
                "reasoning-step-number";

            number.textContent =
                `${index + 1}.`;


            const description =
                document.createElement(
                    "span"
                );

            description.textContent =
                describeToolStep(
                    item
                );


            step.appendChild(
                number
            );

            step.appendChild(
                description
            );


            reasoningSteps.appendChild(
                step
            );
        }
    );
}



askButton.addEventListener(
    "click",
    askQuestion
);


questionInput.addEventListener(
    "keydown",
    (
        event
    ) => {

        if (
            event.key ===
                "Enter"
            &&
            !event.shiftKey
        ) {

            event.preventDefault();

            askQuestion();
        }
    }
);


window.addEventListener(
    "resize",
    () => {

        camera.aspect =
            viewer.clientWidth /
            viewer.clientHeight;


        camera.updateProjectionMatrix();


        renderer.setSize(
            viewer.clientWidth,
            viewer.clientHeight
        );
    }
);


loadScene();

animate();