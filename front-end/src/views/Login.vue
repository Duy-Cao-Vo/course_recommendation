<template>
  <div class="login-space">
    <a-card
      title="Log in to your account"
      :bordered="false"
      style="width: 400px"
    >
      <a-input
        class="email-input"
        type="email"
        placeholder="Email"
        @change="inputEmail"
        @keyup.enter="onClickLogin"
      >
        <a-icon slot="addonBefore" type="mail" style="transform: scale(1.25)" />
      </a-input>
      <a-input
        class="email-input"
        placeholder="Password"
        type="password"
        @change="inputPassword"
        @keyup.enter="onClickLogin"
      >
        <a-icon slot="addonBefore" type="lock" style="transform: scale(1.25)" />
      </a-input>
      <a-button
        type="primary"
        @click="onClickLogin"
        class="log-in-btn"
        style="
          width: 100%;
          font-size: 16px;
          border-radius: 0px;
          margin-top: 15px;
          margin-bottom: 15px;
        "
      >
        Log In
      </a-button>
      <p>
        New to Search Course?<a
          href="/sign-up"
          style="font-weight: 600; color: green !important"
        >
          Sign up</a
        >
      </p>
    </a-card>
  </div>
</template>

<script>
import axios from "axios";
import jwt_decode from "jwt-decode";
export default {
  name: "Login",
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
    inputEmail(value) {
      this.email = value.target.value;
    },
    inputPassword(value) {
      this.password = value.target.value;
    },
    async onClickLogin() {
      if (this.email != "" && this.password != "") {
        this.$message.loading({ content: 'Waiting...', key: "login" });
        await axios({
          method: "POST",
          url: "api/token/",
          data: {
            email: this.email,
            password: this.password,
          },
        })
          .then((res) => {
            localStorage.setItem("token", res.data.access);
            let now = new Date();
            console.log(now.getDate())
            localStorage.setItem("token_date", now.getDate())
            if(jwt_decode(localStorage.getItem("token")).is_dataadmin){
              this.$router.push({
                path: `/dashboard`,
              });
            }
            else {
              this.$router.push({
                path: `/`,
              });
            }
            this.$router.go(this.$router.currentRoute);
            this.$message.success({ content: 'Log in success!', key: "login", duration: 2 });
          })
          .catch((err) => console.log(err));
      } else {
        console.log("Kiểm tra các thông tin nhập vào");
      }
    },
  },
};
</script>

<style>
.email-input .ant-input-group-addon {
  width: 0px !important;
}
.login-space .ant-card-head-title {
  font-size: 20px;
}
.login-space .ant-card {
  margin-left: auto;
  margin-right: auto;
  border: 1px solid green;
  padding: 0px 5px 20px 5px;
  margin-top: 50px;
}
.login-space .email-input {
  padding-bottom: 15px;
  /* padding-bottom: 5px; */
}
.signup-space i, .login-space i {
  position: relative;
  top: -3px !important;
}
</style>