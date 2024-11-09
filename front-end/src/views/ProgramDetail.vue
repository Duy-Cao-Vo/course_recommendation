<script>
import CourseGroupInProgram from "@/components/CourseGroupInProgram.vue";
import axios from "axios";
export default {
  name: "ProgramDetail",
  props: {
    program: Object,
  },
  data() {
    return {
      localProgram: this.program,
    };
  },
  components: {
    CourseGroupInProgram,
  },
  created() {
    this.getProgramData();
  },
  methods: {
    async getProgramData() {
      await axios
        .get(`api/get_program/`, {
          params: {
            id: Number(this.$route.params.id),
          },
        })
        .then((res) => {
          if (res.data.course.length != 0) {
            this.localProgram = res.data;
            document.title = this.localProgram.proName + " | Course Search";
          } else {
            this.localProgram = null;
          }
          console.log(this.localProgram);
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
  computed: {
    skillCover() {
      let array = [];
      this.localProgram.course.forEach((course) => {
        let knowledge = course.knowledge.map((value) => value.value);
        let tool = course.tool.map((value) => value.value);
        let programinglanguage = course.programinglanguage.map(
          (value) => value.value
        );
        let framework = course.framework.map((value) => value.value);
        array = [
          ...array,
          ...knowledge,
          ...tool,
          ...programinglanguage,
          ...framework,
        ];
      });
      return array.filter((v, i, a) => a.indexOf(v) === i);
    },
    image() {
      if (!this.localProgram) return null;
      if (this.localProgram.course[0].crsLink.indexOf("coursera") !== -1)
        return "https://149357281.v2.pressablecdn.com/wp-content/uploads/2020/12/android-chrome-512x512-1.png";
      else if (this.localProgram.course[0].crsLink.indexOf("udemy") !== -1)
        return "https://play-lh.googleusercontent.com/dsCkmJE2Fa8IjyXERAcwc5YeQ8_NvbZ4_OI8LgqyjILpXUfS5YhEcnAMajKPrZI-og";
      else if (this.localProgram.course[0].crsLink.indexOf("edx") !== -1)
        return "https://cdn6.aptoide.com/imgs/b/6/4/b64d193111b31d5a451f5b45a85201f8_icon.png";
      else
        return "https://149357281.v2.pressablecdn.com/wp-content/uploads/2020/12/android-chrome-512x512-1.png";
    },
  },
};
</script>

<style>
.img-program {
  display: block;
  margin-left: auto !important;
  margin-right: auto !important;
  margin-top: 10px;
  width: 80px;
}

@media all and (max-width: 600px) {
  .img-program {
    width: 60px;;
  }
}

.gradient_bg {
  background: hsla(120, 100%, 89%, 1);

  background: linear-gradient(
    90deg,
    hsla(120, 100%, 42%, 0.3) 0%,
    hsla(120, 100%, 42%, 0.8) 100%
  );

  background: -moz-linear-gradient(
    90deg,
    hsla(120, 100%, 42%, 0.3) 0%,
    hsla(120, 100%, 42%, 0.8) 100%
  );

  background: -webkit-linear-gradient(
    90deg,
    hsla(120, 100%, 42%, 0.3) 0%,
    hsla(120, 100%, 42%, 0.8) 100%
  );

  filter: progid: DXImageTransform.Microsoft.gradient( startColorstr="#C6FFC6", endColorstr="#00D800", GradientType=1 );
  /* height: 900px; */
  width: 100%;
}
.skill-button {
  background-color: transparent !important;
  color: white !important;
  border-color: white !important;
  font-weight: 600 !important;
  margin: 5px !important;
  border-radius: 100px !important;
  border-width: 2px !important;
  text-transform: capitalize !important;
}
.skill-button:hover {
  background-color: white !important;
  color: rgb(2, 202, 2) !important;
}
.title-list-course {
  margin-top: 10px;
  text-align: center;
  color: rgb(109, 109, 109) !important;
}
.btn-view-page {
  margin-top: 10px !important;
  border-radius: 0px !important;
  background-color: rgb(4, 250, 4) !important;
  color: white !important;
  font-size: 1.2rem !important;
  padding: 0.2rem !important;
  height: fit-content !important;
  border-color: rgb(4, 250, 4) !important;
}
</style>