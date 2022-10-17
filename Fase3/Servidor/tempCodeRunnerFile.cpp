string dot = "digraph G {";
    if (root == NULL)
        return;
    std::queue<node *> q;
    q.push(root);
    while (!q.empty()) {
        root = q.front();
        q.pop();
        if (root->left) {
            q.push(root->left);
            dot += to_string(root->data->precio) + "->" +
                   to_string(root->left->data->precio) + ";";
        }
        if (root->right) {
            q.push(root->right);
            dot += to_string(root->data->precio) + "->" +
                   to_string(root->right->data->precio) + ";";
        }
    }
    dot += "}";
    std::cout << dot << std::endl;
    