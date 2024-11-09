<template>
  <a-card hoverable class="course-card" :loading="loading">
    <a-card-meta>
      <template v-slot:description>
        <p
          style="font-weight: 600; color: black; margin-bottom: 0px !important"
        >
          {{ courseData.crsName }}
          <a-tag v-if="courseData.crsFee == 0" color="green"> Free </a-tag>
        </p>
        <a-rate
          v-if="improveRating"
          :value="improveRating"
          allow-half
          disabled
        />
        <p
          v-if="courseData.crsFee > 0"
          style="font-weight: 600; margin-bottom: 0px !important"
        >
          Fee: {{ courseData.crsFee }}$
        </p>
        <p
          v-if="courseData.crsEnroll && courseData.crsEnroll > 0"
          style="font-weight: 600; margin-bottom: 0px !important"
        >
          Enroll: {{ courseData.crsEnroll.toLocaleString() }} students
        </p>
        <p
          v-if="courseData.instructor && courseData.instructor.length > 0"
          style="font-weight: 600; margin-bottom: 0px !important"
        >
          Instructor: {{ courseData.instructor[0].value }}
        </p>
        <div>
          <a
            :href="courseData.crsLink"
            target="_blank"
            class="btn-detail"
            style="font-weight: 600; margin-bottom: 0px !important"
            >More details</a
          >
        </div>
        <p class="card-action-add" @click="enrollCourse"
          >Add Favorite</p
        >
      </template>
      <template v-slot:avatar>
        <a-avatar :src="image" />
      </template>
    </a-card-meta>
  </a-card>
</template>

<script>
import axios from "axios";
import jwt_decode from "jwt-decode";
export default {
  name: "CourseCard",
  props: {
    courseData: Object,
  },
  methods: {
    roundToHalf(value) {
      var converted = parseFloat(value); // Make sure we have a number
      var decimal = converted - parseInt(converted, 10);
      decimal = Math.round(decimal * 10);
      if (decimal == 5) {
        return parseInt(converted, 10) + 0.5;
      }
      if (decimal < 3 || decimal > 7) {
        return Math.round(converted);
      } else {
        return parseInt(converted, 10) + 0.5;
      }
    },
    async enrollCourse() {
      if (localStorage.getItem("token")) {
        this.$message.loading({ content: "Add successfully!", key: "enroll" });
        let uid = jwt_decode(localStorage.getItem("token")).user_id;
        let course_id = this.courseData.id;
        await axios({
          method: "POST",
          url: "api/enroll_course/",
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
          data: {
            uid: uid,
            course_id: course_id,
          },
        })
          .then(() => {
            this.$message.success({
              content: "Successfully Added!",
              key: "enroll",
            });
          })
          .catch(() =>
            this.$message.info({
              content: "You may have added or completed this course!",
              key: "enroll",
            })
          );
      } else {
        this.$message.info({
          content: "You need to login to use this function!",
          key: "enroll",
        });
        this.$router.push({
          path: `/login`,
        });
      }
    },
  },
  computed: {
    improveRating() {
      if (!this.courseData.crsRating) return null;
      let rating = parseFloat(this.courseData.crsRating).toFixed(2);
      return this.roundToHalf(rating);
    },
    token() {
      return (
        localStorage.getItem("token") &&
        jwt_decode(localStorage.getItem("token")).is_basicuser
      );
    },
    image() {
      if (this.courseData.crsLink.indexOf("coursera") !== -1)
        return "https://149357281.v2.pressablecdn.com/wp-content/uploads/2020/12/android-chrome-512x512-1.png";
      else if (this.courseData.crsLink.indexOf("udemy") !== -1)
        return "https://play-lh.googleusercontent.com/dsCkmJE2Fa8IjyXERAcwc5YeQ8_NvbZ4_OI8LgqyjILpXUfS5YhEcnAMajKPrZI-og";
      else if (this.courseData.crsLink.indexOf("edx") !== -1)
        return "https://cdn6.aptoide.com/imgs/b/6/4/b64d193111b31d5a451f5b45a85201f8_icon.png";
      else
        return "https://149357281.v2.pressablecdn.com/wp-content/uploads/2020/12/android-chrome-512x512-1.png";
    },
  },
};
</script>

<style>
.card-action-detail,
.card-action-add:hover {
  color: white !important;
  border-radius: 5px !important;
  color: green !important;
  text-decoration: underline;
}
.card-action-add {
  display: block;
  position: relative !important;
  margin-top: auto !important;
  font-size: 15px !important;
  font-weight: 600 !important;
  color: rgb(0, 180, 0) !important;
}

.course-card li {
  height: 30px !important;
}
.course-card .ant-card-actions li {
  margin: 0px !important;
  margin-top: 10px !important;
}
.course-card .ant-card-meta-title {
  font-size: 13px !important;
}
.course-card .ant-card-body {
  padding-left: 10px !important;
  padding-top: 10px !important;
  height: max-content;
}
.course-card .ant-card-meta-detail {
  word-break: break-word !important;
  height: inherit !important;
  margin-bottom: 15px !important;
}
.course-card .ant-card-actions {
  position: absolute;
  bottom: 0px;
  width: 100%;
}
.btn-detail {
  color: rgb(0, 180, 0);
  font-size: 15px !important;
  font-weight: 600 !important;
}
.btn-detail:hover {
  color: green !important;
}
.course-card {
  min-width: 32.85% !important;
  max-width: 32.85% !important;
}
@media all and (max-width: 900px) {
  .course-card {
    min-width: 49.4% !important;
    max-width: 49.4% !important;
  }
}
@media all and (max-width: 500px) {
  .course-card {
    min-width: 99.5% !important;
    max-width: 99.5% !important;
  }
}
</style>