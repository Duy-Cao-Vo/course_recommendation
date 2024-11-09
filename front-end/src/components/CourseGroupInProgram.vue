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
            <template v-slot:title>
              <span
                class="title-checklist"
                style="margin-left: 0px !important"
                >Similar Courses</span
              >
            </template>
            <CourseDetail
              style="
                padding-left: 5px !important;
                padding-right: 5px !important;
                margin-bottom: 5px !important;
              "
              v-for="course in localSimilarCourses"
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
  data() {
    return {
      localSimilarCourses: [...this.similarCourses],
    };
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
          this.localSimilarCourses = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>