<template>
  <div class="register-account">
    <a-input
      class="email-input"
      type="email"
      placeholder="Email"
      @change="inputEmail"
    />
    <a-input
      class="password-input"
      type="password"
      placeholder="Password"
      @change="inputPassword"
    />
    <a-button
      type="primary"
      class="register-btn"
      @click="onClickRegister"
    >
      Register
    </a-button>
  </div>
</template>

<script>
export default {
  name: "RegisterAccount",
  props: {
    email: String,
    password: String,
  },
  data() {
    return {
      localEmail: this.email,
      localPassword: this.password,
    };
  },
  methods: {
    inputEmail(event) {
      this.localEmail = event.target.value;
    },
    inputPassword(event) {
      this.localPassword = event.target.value;
    },
    onClickRegister() {
      // Handle registration logic here
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