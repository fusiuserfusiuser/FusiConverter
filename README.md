
# Functional Ultrasound Image Registration

This program lines up functional ultrasound (fUSI) recordings with the Allen mouse brain atlas, and then labels every point in the recording with the brain area it falls in.

Everything happens in [Napari](https://napari.org), an image viewer, with a few extra panels added on the right-hand side.

## Setup (Windows, one time only)

1. Double-click `install_uv.bat`. This installs **uv**, the tool that downloads everything else the program needs.
2. Close the window when it says it's done.

## Starting the program

Double-click `launch_napari_with_widgets.bat`.

## Opening files

In Naparie, use **File → Open File(s)** to open:

- **Recordings**: the `.mat` files from the fUSI system.
- **Atlases**: `.nii` or `.nii.gz` files, e.g. the Allen atlas.

## Typical workflow

The panels on the right are used roughly from top to bottom.

### 1. Place landmarks (*Add Landmark* panel)

Landmarks are points you can recognise in both the recording and the atlas (e.g. a specific blood vessel or structure).

1. Pick the layer (recording or atlas) under **Target Image Layer**.
2. Type a name under **Landmark Name** and click **Add Landmark**.
3. Click on the image to place the landmark.
4. Repeat for the same landmark on the other layer, **using the exact same name** (capitalization matters). If you have already placed landmarks on the recording, the other layer means the atlas, and vice versa.
5. Click **Save Landmarks**. They're stored next to the original file, so you can reload them later with **Load Existing Landmarks**.

You need **at least 3** landmarks with matching names on both layers. More landmarks give a better fit.

### 2. Align to the atlas (*Alignment* panel)

1. Choose the recording as **Layer to be moved** and the atlas as **Fixed layer**.
2. Click **Align to Atlas**. The recording moves, turns and resizes so its landmarks line up with the atlas landmarks.
3. Click **Save Alignment Matrix** to keep the resulting transformation matrix, which can be applied to other images in the future.

### 3. Fine-tune by hand (*Manual Alignment* panel), optional

Use this to fine-tune the alignment after the automatic fit using landmarks.

- **Translate**: shifts the recording (in mm).
- **Rotate**: turns it (in degrees).
- **Scale**: stretches or squeezes it (1 = unchanged).
- **Drag mode (3D)**: move the recording with the mouse instead. **Note**: You need to click it again to deactivate drag mode when you don't want to move the recording anymore.
  - Drag: shift
  - Shift + drag: tilt
  - Ctrl + drag: spin
- **Reset**: undoes your manual changes.
- **Save Alignment Matrix**: saves the result (this replaces any earlier saved transformation matrix).

### 4. Label brain areas (*Register to Atlas Areas* panel)

1. Choose the aligned recording and click **Register to Atlas Areas**.
2. When asked, pick the Allen **annotation** file (click on the folder named "annotation") at the same resolution as the atlas you aligned to (e.g. `annotation_50.nii.gz`). The file `allen_mouse_connectivity_structure_graph.csv` must be in the same folder.
3. A coloured layer showing the brain areas appears on top of the recording. Hover over it to see each area's name in the bar at the bottom of the window.

The panel shows which areas the recording covers most. The full list is printed in the terminal window.

## Files the program creates

Results are saved **next to the original recording**, with extra endings added to its name:

| File | Contains |
|---|---|
| `<recording>.landmarks.json` | Your landmarks |
| `<recording>.alignment.json` | How to move the recording onto the atlas |
| `<recording>.areas.json` | Which brain areas the recording covers, and how much of each |
| `<recording>.areas.npz` | Which brain area each point in the recording belongs to |

## Troubleshooting

- **"Need >=3 matching landmark names"**: check that the landmark names are spelled exactly the same on both layers.
- **"has not been aligned to the atlas yet"**: run step 2 first, or reopen the recording and choose **Yes** to apply its saved alignment.
- **"No voxel ... landed on a labelled atlas structure"**: the alignment is off. Check it in 3D and adjust it.

## For developers

To run from a terminal:

```
uv sync
uv run python scripts/launch_napari_with_widgets.py
```