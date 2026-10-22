(source-credits)=
# Sources and figure credits

The planned text follows the six supplied CS 532 lecture PDFs and the quiz-to-lecture mapping in `quizByLec.md`. The lecture decks identify Enrique Dunn and credit additional contributors on individual sections. Preserve those specific credits when adapting their material; do not infer authorship or reuse permission from filenames alone.

Lecture 1 gives verified source ranges and identifies original versus adapted examples. The geometry section credits M. Pollefeys and D. Cappelleri (PDF page 62); image formation credits John Oliensis (PDF page 104). The notation and matrix-dimension examples in this foundation edition are original explanatory examples.

The pixel-axis diagram in the notation guide is an original project illustration with an editable TikZ source and paired SVG/PDF assets.

Lecture 1 includes three embedded image assets extracted without retouching from the supplied deck: the railway photograph (PDF page 68), fountain input (page 50), and fountain depth output (page 51). Their original individual creators are not identified on those slides; this source uncertainty is retained in the captions and figure register. The source deck is preserved. Twelve additional geometric/workflow diagrams are original project drawings, with paired SVG/PDF and editable TikZ sources. A repository's text license does not automatically establish the reuse permissions of every embedded source figure.

## Reading list named in the lecture

The deck's PDF pages 9–10 name Richard Szeliski's *Computer Vision: Algorithms and Applications* (2010), David M. Mount's CMSC 754 computational-geometry lecture notes (2012), and Xiang Gao and Tao Zhang's *Introduction to Visual SLAM: From Theory to Practice*. These are source-listed further reading; the present chapter was developed from the supplied slides and quizzes rather than claiming those books were consulted in full.

## Lecture 2

`cs532_f25_Week2.pdf` credits M. Pollefeys and D. Cappelleri for geometry (PDF page 2), John Oliensis for image formation (51), Steve Seitz for warping (72), and R. Hartley, A. Zisserman, and M. Pollefeys for estimation, distortion, and two-view geometry (82, 95, 105, 111).

The basketball-court photograph is extracted from PDF page 71, printed slide 72. Its individual photographer and reuse terms are not identified there. The annotated source/rectangular-warp comparison is computed locally from four disclosed approximate corner coordinates. The chosen output aspect ratio is illustrative. Four additional original vector diagrams explain quiz intersections, warp sampling, consensus, and rectified epipolar lines. Editable sources and paired print/web assets are retained in the figure register.

The interactive camera-motion and perspective-warp diagrams are original local SVG visualizations of the chapter models. The perspective explorer also has a paired static SVG/PDF figure for print and no-JavaScript readers, with an editable TikZ source. Its four numbered collinear points have cross-ratio 4/3 before and after the warp.

Lecture 1's rotatable 3D projection scene uses locally bundled Three.js and OrbitControls r180 (MIT license retained with the library). The scene design, math linkage, and static projection diagram are original project work; the library provides rendering and inspection controls.

## Lecture 3

`wk3_cs532s26_ImageFormation+Homographies-1.pdf` credits John Oliensis for image formation (PDF page 2), Steve Seitz for warping (23), and R. Hartley, A. Zisserman, and M. Pollefeys for estimation, robust fitting, distortion, and two-view geometry (33, 46, 56, 62). Repeated source illustrations link to their existing teaching locations rather than being copied again.

Five original vector diagrams cover FOV, ray–plane depth, the numerical projective map, pentagon symmetries, and RANSAC sampling probability. Paired SVG/PDF assets and editable TikZ sources are in `images/lecture03/`. The local SVG sampling simulator is original project code and uses explicitly stated independent match statuses; its complete static explanation and numerical results appear in print. Quiz filenames, printed-title discrepancies, and adapted versus original numerical examples are identified beside the work.

## Lecture 4

`wk4_cs532s26_TwoViewGeometry.pdf` names Enrique Dunn on its title slide; the radial/two-view sections credit R. Hartley, A. Zisserman, and M. Pollefeys (PDF pages 2 and 8). The stereo section credits Rick Szeliski, Pascal Fua, P. Mordohai, and E. Dunn (PDF page 42, printed slide 46). Author metadata embedded in a PDF is not substituted for these visible credits.

The actual toy/plant photographs are extracted unchanged from PDF page 46 (printed slide 50), then paired with original project labels. The window-size result illustration is extracted unchanged from PDF page 66 (printed slide 70). Individual image creators and reuse terms are not identified on these slides; that uncertainty is retained. Original extracted files and editable panel source are preserved.

Four original paired SVG/PDF diagrams explain the third-view intersection, stereo rays, depth sensitivity, and a window crossing a depth boundary. The 3D stereo explorer uses the existing locally bundled Three.js r180/OrbitControls with the retained MIT license. Its scene, mathematical linkage, and static experiment are original project work. No new remote rendering dependency was introduced.

The essential-matrix decomposition was cross-checked against [OpenCV's official camera-geometry documentation](https://docs.opencv.org/4.12.0/d9/d0c/group__calib3d.html). Its role here is implementation verification of four candidates, translation direction, and cheirality; the supplied lecture and independently worked examples remain the teaching sources.
