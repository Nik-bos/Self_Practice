from docx import Document
from docx.shared import Inches
import matplotlib.pyplot as plt
import os

# Create folder for diagrams
if not os.path.exists("tree_images"):
    os.makedirs("tree_images")


# Function to draw trees
def draw_tree(nodes, edges, filename):

    plt.figure(figsize=(5,4))

    for edge in edges:
        x=[nodes[edge[0]][0],nodes[edge[1]][0]]
        y=[nodes[edge[0]][1],nodes[edge[1]][1]]
        plt.plot(x,y)

    for n,(x,y) in nodes.items():
        plt.scatter(x,y)
        plt.text(x,y,n,ha='center',va='center',fontweight='bold')

    plt.axis("off")
    plt.savefig("tree_images/"+filename,bbox_inches="tight",dpi=300)
    plt.close()


# --------------------------------
# Example Trees
# --------------------------------

examples = {

"Full Binary Tree":[

# Easy
(
{"A":(0,2),"B":(-1,1),"C":(1,1),"D":(-1.5,0),"E":(-0.5,0),"F":(0.5,0),"G":(1.5,0)},
[("A","B"),("A","C"),("B","D"),("B","E"),("C","F"),("C","G")]
),

# Medium
(
{"A":(0,3),"B":(-1,2),"C":(1,2),"D":(-1.5,1),"E":(-0.5,1),"F":(0.5,1),"G":(1.5,1)},
[("A","B"),("A","C"),("B","D"),("B","E"),("C","F"),("C","G")]
),

# Hard
(
{"A":(0,3),"B":(-2,2),"C":(2,2),"D":(-3,1),"E":(-1,1),"F":(1,1),"G":(3,1),"H":(-3.5,0),"I":(-2.5,0)},
[("A","B"),("A","C"),("B","D"),("B","E"),("C","F"),("C","G"),("D","H"),("D","I")]
),

# Hard
(
{"A":(0,3),"B":(-1.5,2),"C":(1.5,2),"D":(-2.5,1),"E":(-0.5,1),"F":(0.5,1),"G":(2.5,1)},
[("A","B"),("A","C"),("B","D"),("B","E"),("C","F"),("C","G")]
),

# Hard
(
{"A":(0,3),"B":(-2,2),"C":(2,2),"D":(-3,1),"E":(-1,1),"F":(1,1),"G":(3,1)},
[("A","B"),("A","C"),("B","D"),("B","E"),("C","F"),("C","G")]
)

],

"Pathological Binary Tree":[

(
{"A":(0,4),"B":(0,3),"C":(0,2),"D":(0,1),"E":(0,0)},
[("A","B"),("B","C"),("C","D"),("D","E")]
),

(
{"A":(0,4),"B":(-1,3),"C":(-2,2),"D":(-3,1),"E":(-4,0)},
[("A","B"),("B","C"),("C","D"),("D","E")]
),

(
{"A":(0,4),"B":(1,3),"C":(2,2),"D":(3,1),"E":(4,0)},
[("A","B"),("B","C"),("C","D"),("D","E")]
),

(
{"A":(0,4),"B":(-1,3),"C":(0,2),"D":(1,1),"E":(2,0)},
[("A","B"),("B","C"),("C","D"),("D","E")]
),

(
{"A":(0,4),"B":(0,3),"C":(-1,2),"D":(-2,1),"E":(-3,0)},
[("A","B"),("B","C"),("C","D"),("D","E")]
)

]

}


# --------------------------------
# Word Document
# --------------------------------

doc=Document()

section=doc.sections[0]
section.top_margin=Inches(0.5)
section.bottom_margin=Inches(0.5)
section.left_margin=Inches(0.5)
section.right_margin=Inches(0.5)

doc.add_heading("Types of Binary Tree",level=1)

doc.add_paragraph("""
There’re mainly 4 types of Binary Tree.
1. Full Binary Tree
2. Complete Binary Tree
3. Perfect Binary Tree
4. Balanced Binary Tree
5. Pathological Binary Tree
""")

doc.add_paragraph("""
1. Full Binary Tree: In Full Binary Tree, every node has either 2 or 0 child nodes. Leaf node will have zero and it is valid.

2. Complete Binary Tree:
a. Every node should have 2 child nodes except last level.
b. If it is a last level, then child nodes should start from left.
c. We cannot break the left to right pattern in the last level.

3. Perfect Binary Tree: If all the internal nodes have exactly 2 children and all the leaf nodes are present in the same level, the tree is called a Perfect Binary Tree.

4. Balanced Binary Tree:
Formula: |Height of Left Subtree – Height of Right Subtree|
If the difference is 0 or 1 for every node, it is balanced.

5. Pathological Binary Tree: When every parent node has only one child node.
""")

# Insert examples
for tree_type,data in examples.items():

    doc.add_heading(tree_type,level=2)

    for i,(nodes,edges) in enumerate(data):

        filename=f"{tree_type}_{i}.png"
        draw_tree(nodes,edges,filename)

        doc.add_paragraph(f"Example {i+1}")
        doc.add_picture("tree_images/"+filename,width=Inches(4))


doc.save("Binary_Tree_Types_Notes.docx")

print("Word file created successfully!")