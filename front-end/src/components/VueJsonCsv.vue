<template>
  <button @click="downloadCsv">Download CSV</button>
</template>

<script>
export default {
  name: "JsonCSV",
  props: {
    data: {
      type: Array,
      required: true
    },
    filename: {
      type: String,
      default: "data.csv"
    }
  },
  methods: {
    downloadCsv() {
      const csvContent = this.convertToCsv(this.data);
      const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
      const link = document.createElement("a");
      if (link.download !== undefined) {
        const url = URL.createObjectURL(blob);
        link.setAttribute("href", url);
        link.setAttribute("download", this.filename);
        link.style.visibility = "hidden";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      }
    },
    convertToCsv(data) {
      const array = [Object.keys(data[0])].concat(data);
      return array
        .map(row => {
          return Object.values(row)
            .map(value => {
              return typeof value === "string" ? `"${value.replace(/"/g, '""')}"` : value;
            })
            .join(",");
        })
        .join("\r\n");
    }
  }
};
</script>