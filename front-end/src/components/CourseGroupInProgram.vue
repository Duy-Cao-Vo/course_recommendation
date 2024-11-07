<template>
  <div>
    <a-row type="flex" class="justify-screen course-tabs">
      <a-col :xs="24" :md="3" :lg="3">
        <p class="style-index-course">Course</p>
        <p class="style-index-value">{{ index + 1 }}</p>
      </a-col>
      <a-col :xs="24" :md="21" :lg="16" class="border-item">
        <CourseDetail :courseDetail="baseCourse"></CourseDetail>
        <a-menu
          :default-selected-keys="['1']"
          mode="inline"
          class="course-similar"
        >
          <a-sub-menu key="Knowledges" class="title-similar">
            <span
              class="title-checklist"
              style="margin-left: 0px !important"
              slot="title"
              >Similar Courses</span
            >
            <CourseDetail
              style="
                padding-left: 5px !important;
                padding-right: 5px !important;
                margin-bottom: 5px !important;
              "
              v-for="course in similarCourses"
              :key="course.id"
              :courseDetail="course"
            ></CourseDetail>
          </a-sub-menu>
        </a-menu>
      </a-col>
    </a-row>
  </div>
</template>

<script>
import CourseDetail from "@/components/CourseDetail.vue";
import axios from "axios";
export default {
  name: "CourseGroupInProgram",
  components: {
    CourseDetail,
  },
  props: {
    baseCourse: Object,
    similarCourses: Object,
    index: Number,
  },
  created() {
    this.getSimilarCourses();
  },
  methods: {
    async getSimilarCourses() {
      await axios
        .get(`api/similar_courses/`, {
          params: {
            id: this.baseCourse.id,
          },
        })
        .then((res) => {
          this.similarCourses = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

<style lang="scss">
.title-similar .ant-menu-submenu-title {
  padding-left: 10px !important;
  padding-right: 100px !important;
  background-color: rgb(245, 245, 245);
  margin-bottom: 0px !important;
  margin-top: 0px !important;
}
.course-similar {
  padding-left: 1px !important;
  padding-right: 1px !important;
  border-left: 1px solid rgb(233, 233, 233) !important;
  border-right: 1px solid rgb(233, 233, 233) !important;
  border-bottom: 1px solid rgb(233, 233, 233) !important;
  border-radius: 1px !important;
  background-color: rgb(245, 245, 245) !important;
}
.title-similar .ant-menu {
  padding-left: 10px !important;
  padding-right: 10px !important;
  padding-bottom: 5px !important;
  background-color: rgb(245, 245, 245) !important;
}
.course-tabs .ant-tabs-bar {
  margin-bottom: 0px !important;
  font-weight: 600;

  // margin-left: 3.5rem !important;
}
.border-item {
  border-bottom: 4px solid rgb(228, 228, 228);
  padding-bottom: 20px;
}
.course-tabs .ant-tabs-tab-active,
.course-tabs .ant-tabs-tab:hover {
  color: rgb(68, 211, 68) !important;
  // margin-left: 3.5rem !important;
}
.course-tabs .ant-tabs-ink-bar {
  color: rgb(68, 211, 68) !important;
  background-color: rgb(68, 211, 68) !important;
}
.style-index-course {
  font-size: 1.4rem;
  font-weight: 500 !important;
  color: rgb(68, 211, 68) !important;
  padding-top: 40px !important;
  margin-bottom: 0px !important;
  text-align: center;
}
.style-index-value {
  font-size: 2.8rem;
  font-weight: 500 !important;
  color: rgb(68, 211, 68) !important;
  text-align: center;
  margin-top: -10px;
}
@media all and (max-width: 767.6px) {
  .style-index-course {
    font-size: 1.6rem !important;
    font-weight: 500 !important;
    color: rgb(68, 211, 68) !important;
    padding-top: 0px !important;
    text-align: center;
    margin-bottom: 0px !important;
  }
  .style-index-value {
    font-size: 2.8rem;
    font-weight: 500 !important;
    color: rgb(68, 211, 68) !important;
    text-align: center;
    margin-bottom: -5px;
    margin-top: -10px;
  }
}
</style>