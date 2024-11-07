<template>
  <a-row type="flex" justify="center" class="manage-learning-tabs">
    <a-col :xs="24" :lg="18">
      <span class="title-manage-learning">Your courses</span>
    </a-col>
    <a-col :xs="24" :lg="18">
      <a-tabs default-active-key="1">
        <a-tab-pane key="1" tab="Favorite">
          <a-select
                show-search
                placeholder="Select website"
                option-filter-prop="children"
                style="
                  top: -12px;
                  width: 200px;
                  float: right !important;
                  margin-top: 20px;
                "
                :filter-option="filterOption"
                @change="(value)=> this.webFavorite = value"
                :value="webFavorite"
              >
                <a-select-option
                  v-for="value in webs"
                  :key="value"
                  :value="value"
                >
                  {{ value }}
                </a-select-option>
              </a-select>
          <CourseEnroll
            v-for="course in show_favorite"
            v-bind:key="course.id"
            v-bind:courseDetail="course"
            style="margin-top: 10px"
            v-bind:removeCoure="removeCourseFromEnroll"
            v-bind:moveToComplete="moveCourseToCompleted"
          ></CourseEnroll>
        </a-tab-pane>
        <a-tab-pane key="2" tab="Completed">
          <a-select
                show-search
                placeholder="Select website"
                option-filter-prop="children"
                style="
                  top: -12px;
                  width: 200px;
                  float: right !important;
                  margin-top: 20px;
                "
                :filter-option="filterOption"
                @change="(value)=> this.webComplete = value"
                :value="webComplete"
              >
                <a-select-option
                  v-for="value in webs"
                  :key="value"
                  :value="value"
                >
                  {{ value }}
                </a-select-option>
              </a-select>
          <CourseComplete
            v-for="course in show_complete"
            v-bind:key="course.id"
            v-bind:courseDetail="course"
            style="margin-top: 10px"
            v-bind:removeCoure="removeCourseFromComplete"
            v-bind:moveToEnroll="moveCourseToEnroll"
          ></CourseComplete>
        </a-tab-pane>
      </a-tabs>
    </a-col>
  </a-row>
</template>

<script>
import CourseEnroll from "@/components/CourseEnroll.vue";
import CourseComplete from "@/components/CourseComplete.vue";
import axios from "axios";
import jwt_decode from "jwt-decode";
export default {
  name: "ManageLearning",
  data() {
    return {
      enroll_courses: [],
      complete_courses: [],
      webs: [],
      webComplete: "All",
      webFavorite: "All"
    };
  },
  components: {
    CourseEnroll,
    CourseComplete,
  },
  created() {
    this.getWeb()
    if (!localStorage.getItem("token")) {
      this.$router.push({
        path: `/`,
      });
    } else {
      this.fetchEnrollCourse();
      this.fetchCompleteCourse();
    }
  },
  methods: {
    async getWeb() {
      await axios
        .get(`api/get_all_web/`)
        .then((res) => {
          res.data[0].value = res.data[0].value.replace("www.", "");
          this.webs = res.data.map((value) => {
            value.value = value.value.replace("www.", "");
            let result = value.value.slice(0, value.value.indexOf("."));
            return result.charAt(0).toUpperCase() + result.slice(1);
          });
          this.webs.splice(0, 0, "All");
          console.log(this.webs);
          this.freeCourseLoading = false;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    async fetchEnrollCourse() {
      await axios({
        method: "GET",
        url: "api/get_enroll_courses/",
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        params: {
          uid: jwt_decode(localStorage.getItem("token")).user_id,
        },
      })
        .then((res) => {
          this.enroll_courses = res.data.enroll;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    async fetchCompleteCourse() {
      await axios({
        method: "GET",
        url: "api/get_complete_courses/",
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        params: {
          uid: jwt_decode(localStorage.getItem("token")).user_id,
        },
      })
        .then((res) => {
          this.complete_courses = res.data.complete;
          this.show_complete = res.data.complete;
          console.log(this.complete_courses);
        })
        .catch((err) => {
          console.log(err);
        });
    },
    moveCourseToCompleted(course) {
      this.complete_courses.push(course);
      let index = this.enroll_courses.indexOf(course);
      if (index > -1) {
        this.enroll_courses.splice(index, 1);
      }
    },
    moveCourseToEnroll(course) {
      this.enroll_courses.push(course);
      let index = this.complete_courses.indexOf(course);
      if (index > -1) {
        this.complete_courses.splice(index, 1);
      }
    },
    removeCourseFromEnroll(course) {
      let index = this.enroll_courses.indexOf(course);
      if (index > -1) {
        this.enroll_courses.splice(index, 1);
      }
    },
    removeCourseFromComplete(course) {
      let index = this.complete_courses.indexOf(course);
      if (index > -1) {
        this.complete_courses.splice(index, 1);
      }
    },
  },
  computed: {
    show_complete() {
      if (this.webComplete != "All") {
        return this.complete_courses.filter((item) =>
          item.crsLink.includes(this.webComplete.toLowerCase())
        );
      } else {
        return this.complete_courses;
      }
    },
    show_favorite() {
      if (this.webFavorite != "All") {
        return this.enroll_courses.filter((item) =>
          item.crsLink.includes(this.webFavorite.toLowerCase())
        );
      } else {
        return this.enroll_courses;
      }
    }
  }
};
</script>

<style lang="scss">
.title-manage-learning {
  border-bottom: 2px solid rgb(68, 211, 68);
  font-size: 27px;
  font-weight: 700;
}
.manage-learning-tabs .ant-tabs-bar {
  margin-bottom: 0px !important;
  font-weight: 600;
  // margin-left: 3.5rem !important;
}
.manage-learning-tabs .ant-tabs-tab-active,
.manage-learning-tabs .ant-tabs-tab:hover {
  color: rgb(68, 211, 68) !important;
  // margin-left: 3.5rem !important;
}
.manage-learning-tabs .ant-tabs-ink-bar {
  color: rgb(68, 211, 68) !important;
  background-color: rgb(68, 211, 68) !important;
}
.manage-learning-tabs .ant-tabs-tab {
  text-transform: capitalize;
}
</style>
