export const format = (node, formatFunction) => {
  function updateValue(e) {
    node.value = formatFunction(node.value);
  }

  node.addEventListener("input", updateValue);
  node.addEventListener("paste", updateValue);

  // Format on intial hydration
  node.value = formatFunction(node.value);

  return {
    destroy() {
      node.removeEventListener("input", updateValue);
      node.removeEventListener("paste", updateValue);
    },
  };
};

export const cardNumber = (value) => {
  const regex = /^(\d{0,4})(\d{0,4})(\d{0,4})(\d{0,4})$/g;
  const onlyNumbers = value.replace(/[^\d]/g, "");

  return onlyNumbers.replace(regex, (regex, $1, $2, $3, $4) =>
    [$1, $2, $3, $4].filter((group) => !!group).join(" ")
  );
};
