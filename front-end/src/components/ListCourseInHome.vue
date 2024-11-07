<template>
  <a-row
    v-if="showCourses.length > 0"
    type="flex"
    class="justify-screen popular-tabs"
    style="margin-bottom: 15px !important"
  >
  <a-col :xs="24" :md="16" :lg="16">

      <span class="title-popular">{{ title }}</span>
  </a-col>
    <a-col :xs="24" :md="16" :lg="15">
      <CourseDetail
        style="margin-top: 15px"
        class="course-home"
        v-for="course in showCourses"
        v-bind:key="course.id"
        v-bind:courseDetail="course"
      />
      <a-button
        v-if="!expand"
        type="primary"
        @click="onClickShowMore"
        class="btn-show"
      >
        Show more  <span style="position: relative; top: -3px !important; margin-left: 3px"> <a-icon type="caret-down" class= "arrow-up" /></span>
      </a-button>
      <a-button
        v-if="expand"
        type="primary"
        @click="onClickShowLess"
        class="btn-show"
      >
        Show less  <span style="position: relative; top: -3px !important; margin-left: 3px"> <a-icon type="caret-up" class= "arrow-up" /></span>
      </a-button>
    </a-col>
  </a-row>
</template>

<script>
import CourseDetail from "@/components/CourseDetail.vue";
import { FEConstants } from "../FEConstants";

export default {
  name: "ListCourseInHome",
  props: {
    title: String,
    listCourse: Array,
  },
  data() {
    return {
      showCourses: [],
      expand: false,
    };
  },
  components: {
    CourseDetail,
  },
  methods: {
    onClickShowMore() {
      this.expand = true;
      this.showCourses = this.listCourse;
    },
    onClickShowLess() {
      this.expand = false;
      this.showCourses = this.listCourse.slice(
        0,
        FEConstants.NUMBER_COURSE_SUMMARIZE
      );
    },
  },
  mounted() {
    this.showCourses = this.listCourse.slice(
        0,
        FEConstants.NUMBER_COURSE_SUMMARIZE
      );
  },

  watch: {
    listCourse: function () {
      this.showCourses = this.listCourse.slice(
        0,
        FEConstants.NUMBER_COURSE_SUMMARIZE
      );
    }
}
};
</script>

<style lang="scss">
@font-face {
  font-family: "Myriad Pro";
  src: url("https://fonts.cdnfonts.com/s/492/MYRIADPRO-REGULAR.woff")
    format("woff");
}
.btn-show:hover {
  color: black !important
}
.btn-show {
  font-family: "Myriad Pro";
  font-size: 22px !important;
  font-weight: 600 !important;
  height: 40px !important;
  display: block !important;
  margin: auto !important;
  margin-top: 15px !important;
  background-color: rgb(226, 226, 226) !important;
  border-color: rgb(226, 226, 226) !important;
  color: rgb(120, 120, 120) !important;
}
.course-home .ant-card-actions{
  margin-left: auto !important;
  margin-right: 20px !important;
  margin-bottom: 20px !important;
}
.arrow-up {
  font-weight: 800 !important;
  font-size: 24px !important;  
  width: fit-content;
  height: fit-content;
  top: -100px !important;
  // padding-bottom: 20px !important;
  svg {
    font-family: "Myriad Pro" !important;
  }
}
.btn-show-more {
  &:focus,
  &:hover {
    border-color: beige !important;
    outline: none !important;

    box-shadow: none !important;
  }
}
.btn-show-more:hover {
  background: rgb(255, 255, 255);
  background: linear-gradient(
    180deg,
    rgba(255, 255, 255, 1) 0%,
    rgba(106, 106, 106, 1) 100%,
    rgba(0, 212, 255, 1) 100%
  );
  font-size: 25px !important;
}
@media all and (max-width: 900px) {
  .course-detail .ant-card-body {
    width: 57%;
  }
  .button-add,
  .button-detail {
    font-size: 13px !important;
    padding: 0px 10px !important;
  }
  .course-detail .ant-card-actions {
    width: fit-content !important;
    margin-left: auto !important;
    margin-right: auto !important;
  }
}
@media all and (max-width: 600px) {
  .course-home .ant-card-body {
    width: 55%;
  }
  .button-add,
  .button-detail {
    font-size: 13px !important;
    padding: 0px 10px !important;
    position: relative !important;
  }
  .course-home .ant-card-actions {
    margin-left: 0px !important;
    margin-right: 0px !important;
  }
}
</style>