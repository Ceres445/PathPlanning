# RRT
 1. Generating random points and checking becomes very slow very quick
 2. Backtracking correct uses more computation, could be easily taken care of during node generation
 3. Can be optimised by tweaking point generation
    - Generate points that are right next to nodes
    - Generate orthogonal lines ( maze only has straight walls)
    - generate lines of minimum length (1)
    - generate a list of valid nodes and choose from it

