# AI-Car-Controller
Developed an AI controller for a car that participated in a race with other cars.


# MODEL: Regression Tree in Python Using Scikit-learn

As we consider the target attributes acceleration, gear, brakes and steering which are continues and numeric values so that’s why we used the regression model. When we use a decision tree to predict a number, it’s called a regression tree. When our goal is to group things into categories (=classify them),then our decision tree is a classification tree. We’ll create a regression tree to predict a numerical value.

# Reason:

Decision tree builds regression or classification models in the form of a tree structure. It breaks down a dataset into smaller and smaller subsets while at the same time an associated decision tree is incrementally developed. The final result is a tree with decision nodes and leaf nodes. A decision node (e.g., Outlook) has two or more branches (e.g., Sunny, Overcast and Rainy), each representing values for the attribute tested. Leaf node (e.g., Hours Played) represents a decision on the numerical target. The topmost decision node in a tree which corresponds to the best predictor called root node. Decision trees can handle both categorical and numerical dat

Decision trees are one of the best forms of learning algorithms based on various learning methods. They boost predictive models with accuracy, ease in interpretation, and stability. The tools are also effective in fitting non-linear relationships since they can solve data-fitting challenges, such as regression and classifications

# Advantages of decision tree:

1. Easy to read and interpret
2. Easy to Prepare
3. Less data cleaning required
4. Its fast and not much time taking so it quickly predict the value and return it to the server before timeout

# Training and testing:

We made a dataset by manually playing the game through arrow keys. We made a total data of approximately 350, 000 rows. We split the data into training and testing in 80:20 ratio.

After training we save the data and tested on the testing data and got 91% accuracy.

