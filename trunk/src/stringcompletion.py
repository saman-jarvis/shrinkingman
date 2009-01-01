#!/usr/bin/env python

class TreeNode:
    def __init__(self, char):
        if len(char) != 1:
            raise AssertionError
        self.children = {}
        self.char     = char
        self.word     = None


class StringCompletion:
    def __init__(self, case_sensitive = True):
        self.root           = TreeNode("0")
        self.case_sensitive = case_sensitive
    
    ## Inserts the given string into the tree.
    def insert(self, string):
        if string == None or string == "":
            raise AssertionError
        
        # Ignore case if requested.
        if self.case_sensitive:
            path = string
        else:
            path = str.lower(string)

        # Walk through all chars and add each into the tree.
        node = self.root
        for char in path:
            #print "About to insert child:", char, "below", node.char
            node = self._insert(node, char)

        # Append the complete word to the leaf.
        node.word = string
    
    # Inserts the given char at the given root position.
    # If root is None a new node is returned.
    # Returns the newly inserted node.
    def _insert(self, root, char):
        if not root:
            raise AssertionError
        if not char:
            raise AssertionError
        if not root.children.has_key(char):
            root.children[char] = TreeNode(char)
        return root.children[char]
        
    ## Finds the given string in the tree.
    ## If exact_match is True (default):
    ##    This function returns the given string if a match
    ##    was found, None otherwise.
    ## If exact_match is False:
    ##    This function returns the given string if an exact match was found.
    ##    Otherwise, it returns a string that starts with the given string.
    ##    If multiple strings start with the given string, this function
    ##    returns the first one alphabetically.
    def find(self, string, exact_match = True):
        if string == None or string == "":
            raise AssertionError

        # Ignore case if requested.
        if self.case_sensitive:
            path = string
        else:
            path = str.lower(string)
        
        # Ascend up the tree until we find a match or a leaf.
        node = self.root
        for char in path:
            if not node.children.has_key(char):
                return None
            node = node.children[char]

        # Now that we point to the node that corresponds with the string,
        # check whether it is in exact match.
        if node.word == string:
            return string
        if exact_match == True:
            return None
        
        # Ascend up the tree until a complete word is found.
        while node.word == None:
            keys = node.children.keys()
            keys.sort()
            node = node.children[keys[0]]
        return node.word


if __name__ == "__main__":
    tree = StringCompletion()
    for string in ("testcompl1", "testcompl2", "dumbtest", "smarttest", "test"):
        tree.insert(string)

    # Exact match
    for string in ("te", "test", "dum", "testcom", "smart"):
      print string + ":", tree.find(string)

    # Leading match
    for string in ("te", "test", "dum", "testcom", "smart"):
      print string + ":", tree.find(string, False)
