<template>
  <a-row type="flex" class="justify-screen popular-tabs" style="background-color: rgb(245, 245, 245)">
    <a-col :xs="24" :lg="18"  style="margin-bottom: 10px">
      <span class="large-title">Topics For You</span>
    </a-col>
    <a-col :xs="24" :lg="17" >
      <a-button
        size="large"
        class="recent-skill-button"
        style="text-transform: capitalize;"
        v-for="item in knowledge"
        :key="item"
        :value="item"
        @click="clickKnowledge"
      >
        {{ item }}
      </a-button>
      <a-button
        size="large"
        class="recent-skill-button"
        style="text-transform: capitalize;"
        v-for="item in platform"
        :key="item"
        :value="item"
        @click="clickPlatform"
      >
        {{ item }}
      </a-button>
      <a-button
        size="large"
        class="recent-skill-button"
        style="text-transform: capitalize;"
        v-for="item in tool"
        :key="item"
        @click="clickTool"
        :value="item"
      >
        {{ item }}
      </a-button>
      <a-button
        size="large"
        class="recent-skill-button"
        style="text-transform: capitalize;"
        v-for="item in programingLanguage"
        :key="item"
        :value="item"
        @click="clickPrograminglanguages"
      >
        {{ item }}
      </a-button>
      <a-button
        size="large"
        class="recent-skill-button"
        style="text-transform: capitalize;"
        v-for="item in framework"
        :key="item"
        :value="item"
        @click="clickFramework"
      >
        {{ item }}
      </a-button>
    </a-col>
  </a-row>
</template>

<script>
import axios from "axios"
export default {
  name: "PopularTopics",
  data() {
    return {
      knowledge: JSON.parse(localStorage.getItem("recentKnowledge")),
      platform: JSON.parse(localStorage.getItem("recentPlatform")),
      tool: JSON.parse(localStorage.getItem("recentTool")),
      programingLanguage: JSON.parse(
        localStorage.getItem("recentPrograminglanguage")
      ),
      framework: JSON.parse(localStorage.getItem("recentFramework")),
    };
  },
  async created() {
    if (this.knowledge) {
      this.knowledge = this.knowledge.filter((v, i, a) => a.indexOf(v) === i && v);
    }

    if (this.platform) {
      this.platform = this.platform.filter((v, i, a) => a.indexOf(v) === i && v);
    }
    if (this.tool) {
      this.tool = this.tool.filter((v, i, a) => a.indexOf(v) === i && v);
    }
    if (this.programingLanguage) {
      this.programingLanguage = this.programingLanguage.filter((v, i, a) => a.indexOf(v) === i && v);
    }
    if (this.framework) {
      this.framework = this.framework.filter((v, i, a) => a.indexOf(v) === i && v);
    }
    await this.fetchData()
  },
  methods: {
    isShow() {
      if (
        (this.knowledge && this.knowledge.length) ||
        (this.platform && this.platform.length) ||
        (this.programingLanguage && this.programingLanguage.length)||
        (this.tool && this.tool.length) ||
        (this.framework && this.framework.length)
      ) {
        return true;
      }
      return false;
    },
    async fetchData() {
      if(!this.isShow()) {
        await axios
        .get(`api/get_skill/`)
        .then((res) => {
          this.knowledge = res.data.knowledges.slice(0,4).map(value=> value.value);
          this.platform = res.data.platforms.slice(0,4).map(value=> value.value);
          this.programinglanguage = res.data.programinglanguages.slice(0,4).map(value=> value.value);
          this.tool = res.data.tools.slice(0,4).map(value=> value.value);
          this.framework = res.data.frameworks.slice(0,4).map(value=> value.value)
        })
        .catch((err) => {
          console.log(err);
        });
      }
    },
    clickPlatform(value) {
      this.$router.push({
        path: `/properties`,
        query: { value: value.target.value, type: "platform" },
      });
    },
    clickKnowledge(value) {
      this.$router.push({
        path: `/properties`,
        query: { value: value.target.value, type: "knowledge" },
      });
    },
    clickTool(value) {
      this.$router.push({
        path: `/properties`,
        query: { value: value.target.value, type: "tool" },
      });
    },
    clickPrograminglanguages(value) {
      this.$router.push({
        path: `/properties`,
        query: { value: value.target.value, type: "programinglanguage" },
      });
    },
    clickFramework(value) {
      this.$router.push({
        path: `/properties`,
        query: { value: value.target.value, type: "framework" },
      });
    },
    // isShow() {
    //   if (
    //     (this.knowledge && this.knowledge.length) ||
    //     (this.platform && this.platform.length) ||
    //     (this.technique && this.technique.length) ||
    //     (this.programingLanguage && this.programingLanguage.length) ||
    //     (this.tool && this.tool.length) ||
    //     (this.framework && this.framework.length)
    //   ) {
    //     return true;
    //   }
    //   return false;
    // },
  },
  computed: {
    // knowledges() {
    //   if(!this.knowledge) {
    //         return JSON.parse(localStorage.getItem("knowledges"))
    //         .map((e) => e.value)
    //         .slice(0, 10);
    //   }
    //   return 0;
    // },
    
  },
};
</script>

<style>
.recent-skill-button {
  border-color: rgb(153, 153, 153) !important;
  color: rgb(153, 153, 153) !important;
  font-weight: 700 !important;
  margin: 0px 5px 10px 5px !important;
}

.recent-skill-button:hover {
  color: green !important;
  border-color: green !important;
}
.hide-title-popular-topic {
  display: none !important;
}
</style>