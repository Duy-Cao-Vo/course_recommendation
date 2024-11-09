<template>
  <a-card hoverable style="width: 100% !important" class="flex-display course-detail course-enroll">
    <template v-slot:cover>
      <img class="image" alt="Image" :src="image" style="padding-left: 24px !important;padding-top: 24px !important; width: 40px !important; height: 40px !important" />
    </template>

    <a-card-meta class="card-content-margin">
      <template v-slot:description>
        <a-tabs :default-active-key="1">
          <a-tab-pane
            :key="1"
            tab="Basic Info"
            style="margin-bottom: 10px !important"
          >
            <a :href="courseDetail.crsLink" target="_blank" class="title-link">
              {{ courseDetail.crsName }}
            </a>
            <div
              v-if="!isNaN(courseDetail.crsRating) && courseDetail.crsRating > 0"
              style="margin-bottom: 8px !important"
            >
              <span class="rate-display"
                >{{ courseDetail.crsRating }}&emsp;</span
              >
              <a-rate :value="courseDetail.rating" allow-half disabled />
              <span class="enroll-display" v-if="courseDetail.crsEnroll && courseDetail.crsEnroll > 0"
                >&emsp;(from {{ courseDetail.crsEnroll.toLocaleString() }} students)</span
              >
            </div>
            <div
              v-if="courseDetail.crsFee == 0"
              style="margin-bottom: 8px !important"
            >
              <p style="margin-bottom: 0px !important">
                <strong>Fee:</strong> Free
              </p>
            </div>
            <div
              v-if="courseDetail.crsFee > 0"
              style="margin-bottom: 8px !important"
            >
              <p style="margin-bottom: 0px !important">
                <strong>Fee: </strong> {{courseDetail.crsFee}}$
              </p>
            </div>
            <div v-if="courseDetail.organization[0]" style="margin-bottom: 8px !important"
            >
              <p style="margin-bottom: 0px !important">
                <strong>Organization: </strong> {{courseDetail.organization[0].value}}
              </p>
            </div>
            <div v-if="courseDetail.crsTime" style="margin-bottom: 8px !important"
            >
              <p style="margin-bottom: 0px !important">
                <strong>Time: </strong> {{courseDetail.crsTime}}
              </p>
            </div>
            <p
              class="instructor-display"
              style="margin-bottom: 10px !important"
            >
              <strong>Instructor:</strong> {{ instructor }}
            </p>
          </a-tab-pane>
          <a-tab-pane
            :key="2"
            tab="Skill covered"
            force-render
            style="margin-bottom: 10px !important"
          >
            <div
              class="instructor-display"
              style="margin-bottom: 0px !important"
              v-if="knowledge.length != 0"
            >
              <p style="margin-bottom: 0px !important">
                <strong>Knowledge:</strong>
              </p>
              <div style="margin-left: 20px">
                <a-tag
                  style="margin-bottom: 10px"
                  v-for="provideSkill in knowledge"
                  v-bind:key="provideSkill"
                  color="green"
                >
                  {{ provideSkill }}
                </a-tag>
              </div>
            </div>
            <div
              class="instructor-display"
              style="margin-bottom: 0px !important"
              v-if="platform.length != 0"
            >
              <p style="margin-bottom: 0px !important">
                <strong>Platform:</strong>
              </p>
              <div style="margin-left: 20px">
                <a-tag
                  style="margin-bottom: 10px"
                  v-for="provideSkill in platform"
                  v-bind:key="provideSkill"
                  color="green"
                >
                  {{ provideSkill }}
                </a-tag>
              </div>
            </div>
            <div
              class="instructor-display"
              style="margin-bottom: 0px !important"
              v-if="programinglanguage.length != 0"
            >
              <p style="margin-bottom: 0px !important">
                <strong>Language:</strong>
              </p>
              <div style="margin-left: 20px">
                <a-tag
                  style="margin-bottom: 10px"
                  v-for="provideSkill in programinglanguage"
                  v-bind:key="provideSkill"
                  color="green"
                >
                  {{ provideSkill }}
                </a-tag>
              </div>
            </div>
            <div
              class="instructor-display"
              style="margin-bottom: 0px !important"
              v-if="tool.length != 0"
            >
              <p style="margin-bottom: 0px !important">
                <strong>Tool:</strong>
              </p>
              <div style="margin-left: 20px">
                <a-tag
                  style="margin-bottom: 10px"
                  v-for="provideSkill in tool"
                  v-bind:key="provideSkill"
                  color="green"
                >
                  {{ provideSkill }}
                </a-tag>
              </div>
            </div>
            <div
              class="instructor-display"
              style="margin-bottom: 0px !important"
              v-if="framework.length != 0"
            >
              <p style="margin-bottom: 0px !important">
                <strong>Framework:</strong>
              </p>
              <div style="margin-left: 20px">
                <a-tag
                  style="margin-bottom: 10px"
                  v-for="provideSkill in framework"
                  v-bind:key="provideSkill"
                  color="green"
                >
                  {{ provideSkill }}
                </a-tag>
              </div>
            </div>
          </a-tab-pane>
          <a-tab-pane
            :key="3"
            tab="Prerequisites"
            force-render
            style="margin-bottom: 10px !important"
          >
            <div v-if="req_knowledge.length == 0 && req_platform.length == 0 && req_tool == 0 && req_programinglanguage == 0 && req_framework == 0">
              <p style="margin-left: 15px; color: rqb(20, 20, 20) !important; font-weight: 600">No require</p>
            </div>
            <div
              class="instructor-display"
              style="margin-bottom: 0px !important"
              v-if="req_knowledge.length != 0"
            >
              <p style="margin-bottom: 0px !important">
                <strong>Knowledge:</strong>
              </p>
              <div style="margin-left: 20px">
                <a-tag
                  style="margin-bottom: 10px"
                  v-for="provideSkill in req_knowledge"
                  v-bind:key="provideSkill"
                  color="red"
                >
                  {{ provideSkill }}
                </a-tag>
              </div>
            </div>
            <div
              class="instructor-display"
              style="margin-bottom: 0px !important"
              v-if="req_platform.length != 0"
            >
              <p style="margin-bottom: 0px !important">
                <strong>Platform:</strong>
              </p>
              <div style="margin-left: 20px">
                <a-tag
                  style="margin-bottom: 10px"
                  v-for="provideSkill in req_platform"
                  v-bind:key="provideSkill"
                  color="red"
                >
                  {{ provideSkill }}
                </a-tag>
              </div>
            </div>
            <div
              class="instructor-display"
              style="margin-bottom: 0px !important"
              v-if="req_programinglanguage.length != 0"
            >
              <p style="margin-bottom: 0px !important">
                <strong>Language:</strong>
              </p>
              <div style="margin-left: 20px">
                <a-tag
                  style="margin-bottom: 10px"
                  v-for="provideSkill in req_programinglanguage"
                  v-bind:key="provideSkill"
                  color="red"
                >
                  {{ provideSkill }}
                </a-tag>
              </div>
            </div>
            <div
              class="instructor-display"
              style="margin-bottom: 0px !important"
              v-if="req_tool.length != 0"
            >
              <p style="margin-bottom: 0px !important">
                <strong>Tool:</strong>
              </p>
              <div style="margin-left: 20px">
                <a-tag
                  style="margin-bottom: 10px"
                  v-for="provideSkill in req_tool"
                  v-bind:key="provideSkill"
                  color="red"
                >
                  {{ provideSkill }}
                </a-tag>
              </div>
            </div>
            <div
              class="instructor-display"
              style="margin-bottom: 0px !important"
              v-if="req_framework.length != 0"
            >
              <p style="margin-bottom: 0px !important">
                <strong>Framework:</strong>
              </p>
              <div style="margin-left: 20px">
                <a-tag
                  style="margin-bottom: 10px"
                  v-for="provideSkill in req_framework"
                  v-bind:key="provideSkill"
                  color="red"
                >
                  {{ provideSkill }}
                </a-tag>
              </div>
            </div>
          </a-tab-pane>
        </a-tabs>
      </template>
    </a-card-meta>
  </a-card>
</template>

<script>
import axios from "axios"
import jwt_decode from "jwt-decode"
export default {
  name: "CourseEnroll",
  props: {
    courseDetail: Object,
    removeCoure: Function,
    moveToComplete: Function
  },
  data() {
    return {
      imageCousera: "@/assets/coursera.png",
      imageUdemy: "@/assets/udemy.png",
      imageEdx: "@/assets/edx.png",
      localCourseDetail: { ...this.courseDetail }
    };
  },
  created() {
    this.improveRating();
  },
  computed: {
    instructor() {
      return this.courseDetail.instructor
        .map((value) => value.value)
        .toString();
    },
    token() {
      return localStorage.getItem("token")
    },
    image() {
      if (this.courseDetail.crsLink.indexOf("coursera") !== -1)
        return "https://149357281.v2.pressablecdn.com/wp-content/uploads/2020/12/android-chrome-512x512-1.png";
      else if (this.courseDetail.crsLink.indexOf("udemy") !== -1)
        return "https://play-lh.googleusercontent.com/dsCkmJE2Fa8IjyXERAcwc5YeQ8_NvbZ4_OI8LgqyjILpXUfS5YhEcnAMajKPrZI-og";
      else if (this.courseDetail.crsLink.indexOf("edx") !== -1)
        return "https://cdn6.aptoide.com/imgs/b/6/4/b64d193111b31d5a451f5b45a85201f8_icon.png";
      else
        return "https://149357281.v2.pressablecdn.com/wp-content/uploads/2020/12/android-chrome-512x512-1.png";
    },
    knowledge() {
      return this.courseDetail.knowledge.map((value) => value.value);
    },
    tool() {
      return this.courseDetail.tool.map((value) => value.value);
    },
    programinglanguage() {
      return this.courseDetail.programinglanguage.map((value) => value.value);
    },
    platform() {
      return this.courseDetail.platform.map((value) => value.value);
    },
    framework() {
      return this.courseDetail.framework.map((value) => value.value);
    },
    req_knowledge() {
      return this.courseDetail.require_knowledge.map((value) => value.value);
    },
    req_tool() {
      return this.courseDetail.require_tool.map((value) => value.value);
    },
    req_programinglanguage() {
      return this.courseDetail.require_programinglanguage.map(
        (value) => value.value
      );
    },
    req_platform() {
      return this.courseDetail.require_platform.map((value) => value.value);
    },
    req_framework() {
      return this.courseDetail.require_framework.map((value) => value.value);
    },
  },
  methods: {
    async completeCourse() {
      this.$message.loading({ content: 'Waiting...', key: "complete" });
      this.moveToComplete(this.courseDetail)
      let uid = jwt_decode(localStorage.getItem("token")).user_id;
      let course_id = this.courseDetail.id;
      await axios({
          method: "POST",
          url: "api/complete_course/",
          headers: { 'Authorization': `Bearer ${localStorage.getItem("token")}` },
          data: {
            uid: uid,
            course_id: course_id,
          },
        })
          .then(() => {
            this.$message.success({ content: 'Successfully Completed!', key: "complete" });
          })
          .catch((err) => {
            console.log(err)
            this.$message.info({ content: 'Can not complete this course!', key: "complete" })
          });
    },
    async removeCourse() {
      this.$message.loading({ content: 'Leaving...', key: "leave" });
      this.removeCoure(this.courseDetail)
      let uid = jwt_decode(localStorage.getItem("token")).user_id;
      let course_id = this.courseDetail.id;
      await axios({
          method: "POST",
          url: "api/unenroll_courses/",
          headers: { 'Authorization': `Bearer ${localStorage.getItem("token")}` },
          data: {
            uid: uid,
            course_id: course_id,
          },
        })
          .then(() => {
            this.$message.success({ content: 'Successfully Left!', key: "leave" });
          })
          .catch((err) => {
            console.log(err)
            this.$message.info({ content: 'Can not leave this course!', key: "leave" })
          });
    },
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
    improveRating() {
      this.localCourseDetail.crsRating = parseFloat(
        this.courseDetail.crsRating
      ).toFixed(2);
      this.localCourseDetail.rating = this.roundToHalf(this.localCourseDetail.crsRating);
    },
  },
};
</script>