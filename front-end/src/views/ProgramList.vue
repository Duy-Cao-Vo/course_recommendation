<template>
  <div style="background-color: rgb(253, 253, 253)">
    <a-row
      type="flex"
      class="search-mobile-screen"
      style="margin-bottom: 15px"
    >
      <a-col :xs="24" :lg="{ offset: 3, span: 8 }">
        <span class="large-title">Program Catalog </span>
      </a-col>
    </a-row>
    <a-row type="flex" class="justify-screen search-mobile-screen">
      <a-col
        :xs="8"
        :lg="5"
        class="search-screen max-mobile-screen"
      >
        <a-menu
          class="filter-bar"
          style="width: 100%"
          :default-selected-keys="['1']"
          mode="inline"
        >
          <span class="title-checklist" slot="title">Career</span>
          <a-radio-group :options="this.careers" :value="choosenCareer" @change="(value)=> {
            onChooseCareer(value)
            onClickSearch()
            }" />
        </a-menu>
      </a-col>
      <a-col
        :xs="16"
        :lg="{ offset: 0, span: 13 }"
        class="search-screen max-mobile-screen"
      >
      <a-select
              v-if="programList.length != 0"
              show-search
              placeholder="Select website"
              option-filter-prop="children"
              style="
                top: -12px;
                width: 200px;
                float: right !important;
                margin-top: 9px;
              "
              :filter-option="filterOption"
              @change="selectWeb"
              :value ="valueWeb"
            >
              <a-select-option
                v-for="value in webs"
                :key="value"
                :value="value"
              >
                {{ value }}
              </a-select-option>
            </a-select>
            <h5
              style="
                color: rgb(2, 160, 2) !important;
                overflow: hidden;
                max-height: 100px;
                display: -webkit-box;
                -webkit-line-clamp: 3;
                -webkit-box-orient: vertical;
              "
            >
              {{ programList.length }} results for {{choosenCareer}}
            </h5>
        <div v-if="!this.loadingPrograms">
          <div v-if="this.displayProgram.length > 0">
            <ProgramCard
            v-for="program in displayProgram"
            :programDetail="program"
            :key="program.id"
            style="margin-bottom: 10px !important"
          />
          </div>
          <div v-if="this.displayProgram.length == 0">
            <h2 style="color: rgb(112, 112, 112) !important; font-weight: 700">
              Sorry, we couldn't find any matching results
            </h2>
          </div>
        </div>
        <div v-else>
          <a-card
            :loading="true"
            style="height: 160px !important; min-height: 160px !important; width: 100% !important"
          >
            whatever content
          </a-card>
        </div>
      </a-col>
    </a-row>
  </div>
</template>

<script>
import axios from "axios";
import ProgramCard from "@/components/ProgramCard.vue";
export default {
  name: "ProgramList",
  data() {
    return {
      loadingPrograms: true,
      choosenCareer: "",
      displayProgram: [],
      webs:[],
      valueWeb: "All"
    };
  },
  props: {
    programList: Array,
  },
  components: {
    ProgramCard,
  },
  methods: {
    selectWeb(value) {
      this.valueWeb = value
      if (value != "All") {
        this.displayProgram = this.programList.filter((item) =>
          item.course[0].crsLink.includes(value.toLowerCase())
        );
      } else {
        this.displayProgram = this.programList;
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
    onChooseCareer(value) {
      this.choosenCareer = value.target.value;
    },
    async onClickSearch() {
      let career = JSON.parse(localStorage.getItem("career")).filter(
        (item) => item.creTitle == this.choosenCareer
      );
      this.loadingPrograms = true;
      await axios
        .get(`api/get_program_by_career/`, {
          params: {
            id: career[0].id,
          },
        })
        .then((res) => {
          this.valueWeb = "All"
          this.loadingPrograms = false;
          this.programList = res.data;
          this.displayProgram = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    getProgram(id) {
      this.loadingPrograms = true;
      axios
        .get(`/api/get_program_by_career/`, {
          params: {
            id: id,
          },
        })
        .then((res) => {
          this.valueWeb = "All"
          this.programList = res.data;
          this.displayProgram = res.data
          this.loadingPrograms = false;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    fetchCareer() {
      this.careers = JSON.parse(localStorage.getItem("career")).map(
        (e) => e.creTitle
      );
      this.detailCareer = JSON.parse(localStorage.getItem("career"));
    },
  },
  created() {
    document.title = "Explore Programs And Grow Your Career | Course Search";
    this.getProgram(this.$route.query.career);
    this.fetchCareer();
    this.getWeb()
  },
  watch: {
    $route(to) {
      if (to.name === "ProgramList") {
        document.title =
          "Explore Programs And Grow Your Career | Course Search";
        this.getProgram(this.$route.query.career);
        this.fetchCareer();
      }
    },
  },
};
</script>

<style>
</style>