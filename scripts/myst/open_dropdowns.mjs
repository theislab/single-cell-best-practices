// LaTeX has no handler for dropdowns, cards or tabs and silently drops them with their content.
const printed = process.argv.some((arg) => arg === "--pdf" || arg === "--tex");

function unfold(node) {
  node.children?.forEach(unfold);
  if (node.type === "details") {
    node.type = "admonition";
    delete node.open;
  } else if (node.type === "summary") {
    node.type = "admonitionTitle";
  } else if (node.type === "tabItem") {
    node.type = "div";
    node.children.unshift({
      type: "paragraph",
      children: [
        { type: "strong", children: [{ type: "text", value: node.title }] },
      ],
    });
  } else if (["card", "grid", "tabSet"].includes(node.type)) {
    node.type = "div";
  }
}

export default {
  name: "Open dropdowns in print",
  transforms: [
    {
      name: "open-dropdowns",
      stage: "document",
      plugin: () => (tree) => {
        if (printed) unfold(tree);
      },
    },
  ],
};
