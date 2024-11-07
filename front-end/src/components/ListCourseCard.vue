<template>
  <a-row type="flex" class="justify-screen" :class ="{hide: !courseDatas}">
    <a-col :xs="1">
      <a-icon
        type="left-circle"
        class="align-to-right decor-arrow" :class="{hide:loadingCard}"
        @click="moveCardContainterToRight"
      />
    </a-col>
    <a-col :xs="22" :lg="22">
      <div v-if="!loadingCard" class= "popular-card-container" :id="'card-container' + keyList">
        <CourseCard
          v-for="course in courseDatas"
          v-bind:key="course.id"
          v-bind:courseData="course"
          class="card-margin"
        />
      </div>
      <div v-else class= "popular-card-container" :id="'card-container' + keyList">
        <a-card
          :loading="true"
          class="card-margin"
          style="width: 178px !important; min-width: 178px !important"
        >
          whatever content
        </a-card>
        <a-card
          :loading="true"
          class="card-margin"
          style="width: 178px !important; min-width: 178px !important"
        >
          whatever content
        </a-card>
        <a-card
          :loading="true"
          class="card-margin"
          style="width: 178px !important; min-width: 178px !important"
        >
          whatever content
        </a-card>
        <a-card
          :loading="true"
          class="card-margin"
          style="width: 178px !important; min-width: 178px !important"
        >
          whatever content
        </a-card>
        <a-card
          :loading="true"
          class="card-margin"
          style="width: 178px !important; min-width: 178px !important"
        >
          whatever content
        </a-card>
        <a-card
          :loading="true"
          class="card-margin"
          style="width: 178px !important; min-width: 178px !important"
        >
          whatever content
        </a-card>
      </div>
    </a-col>
    <a-col :xs="1">
      <a-icon
        type="right-circle"
        class="decor-arrow" :class="{hide:loadingCard}"
        @click="moveCardContainterToLeft"
      />
    </a-col>
  </a-row>
</template>

<script>
import CourseCard from "@/components/CourseCard.vue";
import { FEConstants } from "../FEConstants";
export default {
  name: "ListCourseCard",
  components: {
    CourseCard,
  },
  props: {
    keyList: String,
    courseDatas: Array,
    loadingCard: Boolean,
  },
  methods: {
    moveCardContainterToRight() {
      let container = document.getElementById('card-container' + this.keyList);
      let size = container.getElementsByClassName("card-margin")[0].getBoundingClientRect();
      container.scrollLeft = container.scrollLeft -
        FEConstants.NUMBER_CARD_TRANS * (size.width + 5);
      
    },
    moveCardContainterToLeft() {
      let container = document.getElementById('card-container' + this.keyList);
      let size = container.getElementsByClassName("card-margin")[0].getBoundingClientRect();
      container.scrollLeft = container.scrollLeft +
        FEConstants.NUMBER_CARD_TRANS * (size.width + 5);
      
},
  },
};
</script>

<style>
.justify-screen {
  justify-content: center !important;
  width: 100%;
}
.hide {
  display: none !important;
}
.align-to-right {
  position: relative;
  float: right;
}

.decor-arrow {
  position: relative;
  font-size: 2rem;
  top: 30%;
  color: rgb(68, 211, 68) !important;
}

.decor-arrow:hover {
  color: white !important;
  background-color: rgb(68, 211, 68) !important;
  border-radius: 50% !important;
}

.arrow-right {
  position: absolute !important;
}

.popular-card-container {
  display: flex;
  overflow-x: auto;
  overflow-y: hidden;
  margin: 10px !important;
  offset: -100px;
  scroll-behavior: smooth;
}

.popular-card-container::-webkit-scrollbar {
  width: 0 !important;
}

.card-margin {
  margin-right: 5px !important;
}
</style>