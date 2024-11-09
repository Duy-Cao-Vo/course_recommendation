import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';
import SearchBySkill from "../views/SearchBySkill.vue";
import RegisterAccount from "../views/RegisterAccount.vue";
import SearchByCareer from "../views/SearchByCareer.vue";
import ProgramList from "../views/ProgramList.vue";
import ProgramDetail from "../views/ProgramDetail.vue";
import Login from "../views/Login.vue";
import SignUp from "../views/SignUp.vue";
import UpdateInformation from "../views/UpdateInformation.vue";
import ManageLearning from "../views/ManageLearning.vue";
import UserProfile from "../views/UserProfile.vue";
import Crawl from "../views/Crawl.vue";
import AddUser from "../views/AddUser.vue";
import Help from "../views/Help.vue";
import NER from "../views/NER.vue";
import Dashboard from "../views/Dashboard.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/about',
    name: 'About',
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/search-by-skill',
    name: 'SearchBySkill',
    component: SearchBySkill
  },
  {
    path: '/add-user',
    name: 'AddUser',
    component: AddUser
  },
  {
    path: '/help',
    name: 'Help',
    component: Help
  },
  {
    path: '/registeraccount',
    name: 'RegisterAccount',
    component: RegisterAccount
  },
  {
    path: '/user-profile',
    name: 'UserProfile',
    component: UserProfile
  },
  {
    path: '/managelearning',
    name: 'ManageLearning',
    component: ManageLearning
  },
  {
    path: '/searchbycareer',
    name: 'SearchByCareer',
    component: SearchByCareer
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/sign-up',
    name: 'SignUp',
    component: SignUp
  },
  {
    path: '/update-information',
    name: 'UpdateInformation',
    component: UpdateInformation
  },
  {
    path: '/programs',
    name: 'ProgramList',
    component: ProgramList
  },
  {
    path: '/programs/:id',
    name: 'ProgramDetail',
    component: ProgramDetail
  },
  {
    path: '/crawl',
    name: 'Crawl',
    component: Crawl
  },
  {
    path: '/ner/:train_output',
    name: 'NER',
    component: NER
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});

export default router;