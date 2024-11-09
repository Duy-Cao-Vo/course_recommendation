<template>
  <a-card hoverable style="width: 100% !important" class="flex-display course-detail program-card">
    <template v-slot:cover>
      <img class="image" alt="Image" :src="image" />
    </template>
    <template v-slot:actions>
      <a-button
        type="primary"
        class="button-add"
        style="width: 98% !important"
        ghost
        @click="viewDetail"
      >
        Detail
      </a-button>
    </template>

    <a-card-meta class="card-content-margin">
      <template v-slot:description>
        <h3 style="margin-bottom: 0px !important; font-size: 19px !important">
              {{ programDetail.proName }}
            </h3>
        <p class="instructor-display">
          <strong>Number courses:</strong> {{ numberCourse }}
        </p>
      </template>
    </a-card-meta>
  </a-card>
</template>

<script>
export default {
  name: "ProgramCard",
  props: {
    programDetail: Object,
  },
  computed: {
    numberCourse() {
      return this.programDetail.course.length;
    },
    image() {
      if (this.programDetail.course[0].crsLink.indexOf("coursera") !== -1)
        return "https://149357281.v2.pressablecdn.com/wp-content/uploads/2020/12/android-chrome-512x512-1.png";
      else if (this.programDetail.course[0].crsLink.indexOf("udemy") !== -1)
        return "https://play-lh.googleusercontent.com/dsCkmJE2Fa8IjyXERAcwc5YeQ8_NvbZ4_OI8LgqyjILpXUfS5YhEcnAMajKPrZI-og";
      else if (this.programDetail.course[0].crsLink.indexOf("edx") !== -1)
        return "https://cdn6.aptoide.com/imgs/b/6/4/b64d193111b31d5a451f5b45a85201f8_icon.png";
      else
        return "https://149357281.v2.pressablecdn.com/wp-content/uploads/2020/12/android-chrome-512x512-1.png";
    },
  },
  methods: {
    viewDetail() {
      this.$router.push({
        path: `/programs/${this.programDetail.id}`,
      });
    },
  },
};
</script>

<style>
.program-card h3 {
  word-wrap: break-word !important;
  /* word-break: break-all !important; */
}
</style>