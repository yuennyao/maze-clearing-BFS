# Maze Clearing using Breadth-First Search (BFS) Algorithm
<p align="center"><img width="400" alt="Screenshot 2023-09-07 102719" src="https://github.com/yuennyao/maze-clearing-BFS/assets/87840513/691a409e-456d-43b3-8c2f-ab31fbb8f1bd"></p>
<br>
A man is given a rubbish bin that can hold a total of 5&#13221; of objects. He is required to clear out all the rubbish from the rooms in Figure 1. However, he can only move the rubbish bin of 40 kg. Consider the rubbish bin has no weight, and the rubbish has no fixed shape. 

The rubbish is denoted with coloured hexagons with symbols. The sizes of the rubbish are specified by the colour and the weights are specified by the symbols.

Find the path to clear out all the rubbish bins.

<h3>Several assumptions are made to find the solution in this case:<br></h3> 
● A room has the shape of a hexagon and all adjacent rooms are connected. <br>
● All room has the same length of 10m. The path cost can be represented by the number of travel/movements from one room to another room in a ratio of 1:10, which means 1 travel/movement causes 10m of path cost. <br>
● Each room has a maximum of six neighbouring rooms which will be added to a list known as children. <br>
● The man must enter from the first room, with the coordinate (0,0). <br>
● The rubbish bin can only be emptied in the disposal room. <br>
● The rubbish bin must be physically moved from one room to an adjacent room as teleportation is not allowed. <br>
● If the rubbish bin exceeds the man's strength limit, he cannot move the bin to another room. <br>
● Only one rubbish bin is provided, and it cannot be added or destroyed. <br>
● The man is able to explore a room to check the condition of the room before entering the room. All the possible rooms that can be explored are added to a list known as frontier. <br>
● If the man is exploring a rubbish room, he can check the size of the rubbish placed in the room and his strength before entering the room. <br>
● If the man is exploring a disposal room or empty room, he can directly enter a room with the fulfilled conditions. <br>
● A complete path starts from entering a room and ends when: <br> 
  &nbsp;○ reaching a disposal room while carrying a filled rubbish bin <br>
  &nbsp;○ reaching a room where all its neighbouring rooms have been explored or will overload the rubbish bin. <br>
  &nbsp;○ reaching a room where the rooms in frontier cannot be entered due to a mismatch with the children of the room. <br> 
● A room is considered to be explored if the man enters into it. An explored room is added to a list known as explored. <br>
● When the man enters a room with rubbish, it will automatically be deposited into the bin. <br>
● When the man enters a disposal room with the rubbish bin filled with rubbish, the rubbish will be automatically cleared and the bin will be emptied. A new path will start from the current disposal room to continue exploring and entering other neighbouring rooms. <br>
● The man cannot enter the same room multiple times on the same path. Once he enters a room where all its neighbouring rooms have been explored before, a new path is initiated starting from the current room so that all the explored rooms in the previous path can be re-explored. <br>
● The man can enter the same room multiple times on different paths. <br>
● A solution is found and the search is terminated when the man successfully clears all the rubbish from the rubbish rooms in different paths. <br>
