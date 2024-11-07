<template>
  <a-row type="flex" class="justify-screen popular-tabs">
    <a-col :xs="24" :lg="18">
      <span class="title-popular">Top free courses</span>
      <a-select
        show-search
        placeholder="Select website"
        option-filter-prop="children"
        style="width: 200px; float: right !important; margin-top: 9px"
        class="web-select"
        :filter-option="filterOption"
        @change="selectWeb"
        default-value="All"
      >
        <a-select-option v-for="value in webs" :key="value" :value="value">
          {{ value }}
        </a-select-option>
      </a-select>
    </a-col>
    <a-col :xs="24" :lg="18">
      <ListCourseCard
        keyList="free"
        :courseDatas="topFreeCourse"
        :loadingCard="freeCourseLoading"
      ></ListCourseCard>
    </a-col>
  </a-row>
</template>

<script>
import ListCourseCard from "@/components/ListCourseCard.vue";
import axios from "axios";
import { FEConstants } from "../FEConstants";
import jwt_decode from "jwt-decode";
export default {
  name: "ListFreeCourses",
  components: {
    ListCourseCard,
  },
  data() {
    return {
      topFreeCourse: [],
      freeCourseLoading: true,
      webs: [],
    };
  },
  created() {
    this.getFreeCourse();
    this.getWeb();
  },
  methods: {
    async selectWeb(value) {
      this.freeCourseLoading = true;
      let id = -1;
      if (localStorage.getItem("token")) {
        id = jwt_decode(localStorage.getItem("token")).user_id;
      }
      if (value != "All") {
        await axios
          .get(`api/get_free_course_web/`, {
            params: {
              number: FEConstants.NUMBER_CARD_IN_LIST,
              uid: id,
              web: value,
            },
          })
          .then((res) => {
            if (res.data.length >= 5) {
              this.topFreeCourse = res.data;
            } else {
              this.$message.info({
                content: "There is no course avalable now!",
                key: "find",
              });
            }
            this.freeCourseLoading = false;
          })
          .catch((err) => {
            console.log(err);
          });
      } else {
        this.getFreeCourse();
      }
    },
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
    async getFreeCourse() {
      this.freeCourseLoading = true;
      let id = -1;
      if (localStorage.getItem("token")) {
        id = jwt_decode(localStorage.getItem("token")).user_id;
      }
      await axios
        .get(`api/get_free_course/`, {
          params: {
            number: FEConstants.NUMBER_CARD_IN_LIST,
            uid: id,
          },
        })
        .then((res) => {
          this.topFreeCourse = res.data;
          this.freeCourseLoading = false;
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

<style lang="scss">
.web-select {
  margin-right: 4vw !important;
}
@media all and (max-width: 992px) {
  .web-select {
    margin-right: calc(4vw + 15px) !important;
  }
}
.popular-tabs .ant-tabs-bar {
  margin-bottom: 0px !important;
  font-weight: 600;
  // margin-left: 3.5rem !important;
}
.popular-tabs .ant-tabs-tab-active,
.popular-tabs .ant-tabs-tab:hover {
  color: rgb(68, 211, 68) !important;
  // margin-left: 3.5rem !important;
}
.popular-tabs .ant-tabs-ink-bar {
  color: rgb(68, 211, 68) !important;
  background-color: rgb(68, 211, 68) !important;
}
.popular-tabs .ant-tabs-tab {
  text-transform: capitalize;
}
.title-popular {
  border-bottom: 2px solid rgb(68, 211, 68);
  font-size: 27px;
  font-weight: 700;
}
</style>