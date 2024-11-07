<template>
  <div class="signup-card">
    <a-card title="Create new account" :bordered="false">
      <div style="margin-bottom: 16px">
        <a-input addon-before="Email" type="email" @change="updateEmail" />
      </div>
      <div style="margin-bottom: 16px">
        <a-input addon-before="Password" type="password" @change="updatePass" />
      </div>
      <a-button
        type="primary"
        class="button-create-account"
        @click="onClickRegist"
        >Create Account</a-button
      >
    </a-card>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "RegisterAccount",
  props: {
    email: String,
    password: String,
  },
  mounted() {
    if (localStorage.getItem("token")) {
      this.$router.push({
        path: `/`,
      });
    }
  },
  methods: {
    async onClickRegist() {
      await axios
        .post(`api/register/`, {
          email: this.email,
          password: this.password,
        })
        .then(() => {
          console.log("True");
        })
        .catch((err) => {
          console.log(err);
        });
    },
    updateEmail(val) {
      this.email = val.target.value;
    },
    updatePass(val) {
      this.password = val.target.value;
    },
  },
};
</script>

<style>
.signup-card {
  width: 40rem;
  margin-top: 50px;
  margin-bottom: 50px;
  margin-left: auto;
  margin-right: auto;
  text-align: center !important;
  border: 2px solid rgb(0, 255, 42);
  border-radius: 5px;
}
.ant-card-head-title {
  font-size: 1.5rem;
}
.ant-input-group-addon {
  width: 150px !important;
  font-weight: bold !important;
  text-align: left !important;
}
.button-create-account {
  font-size: 1.2em !important;
  font-weight: 450 !important;
  margin-bottom: 10px !important;
  background-color: rgb(68, 211, 68) !important;
  border-color: rgb(68, 211, 68) !important;
}
</style>