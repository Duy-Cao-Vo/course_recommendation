<template>
  <div class="container">
    <div class="tableheader">
      <div>
        <span class="right:margin-1">Show</span>
        <select v-model="currentEntries" class="select-css" @change="paginateEntries">
          <option v-for="se in showEntries" :key="se" :value="se">{{ se }}</option>
        </select> 
        <span class="left:margin-1">entries</span>
      </div>
      <treeselect style="width: 350px; background: #ffe7e8; margin-left: 310px;"
      placeholder="All skill type"
      :multiple="true"
      :options="SkillType"
      :disable-branch-nodes="true"
      v-model="valueSkillType"
      search-nested
      v-on:input="filterColumn"
      v-on:select="filterColumn"
      v-on:deselect="filterColumn"
      v-on:close="filterColumn"
      />
      <treeselect style="width: 130px; margin-left: 5px; align-self: center;"
        :multiple="false"
        :options="RangeScore"
        v-model="valueRangeScore"
        placeholder="All Score"
        v-on:input="filterColumn"
        v-on:select="filterColumn"
        v-on:deselect="filterColumn"
        v-on:close="filterColumn"
      />
      <treeselect style="width: 140px; margin-left: 5px; margin-right: 5px; align-self: center;"
        :multiple="false"
        :options="RangeScore"
        v-model="valueScore"
        placeholder="Choose Score"
        v-on:input="ChooseRangeScore"
        v-on:select="ChooseRangeScore"
        v-on:deselect="ChooseRangeScore"
        v-on:close="ChooseRangeScore"
      />
      <div>
        <input type="search" class="input px:width-25" placeholder="Search here..." v-model="searchInput" 
        @keyup="searchEvent">
      </div>
    </div>
    <table class="table table:border secondary-5:border" 
    style="border:1px solid #ccc; border-radius: 5%; margin-top: 10px;">
      <thead>
        <tr>
          <th v-for="th in tableHeader" :key="th" style="background-color:rgb(4, 220, 4)">
            <div class="between:flex center:items">
              <span><strong>{{ th.text }}</strong></span>
              <span @click.prevent="sortByColumn(th.name)">
                <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="256" height="256" viewBox="0 0 256 256" xml:space="preserve">
                <desc>Created with Fabric.js 1.7.22</desc>
                <defs>
                </defs>
                <g transform="translate(128 128) scale(0.72 0.72)" style="">
                  <g style="stroke: none; stroke-width: 0; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: none; fill-rule: nonzero; opacity: 1;" transform="translate(-175.05 -175.05000000000004) scale(3.89 3.89)" >
                  <circle cx="45" cy="45" r="45" style="stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(62,206,41); fill-rule: nonzero; opacity: 1;" transform="  matrix(1 0 0 1 0 0) "/>
                  <path d="M 51.935 60.03 H 38.065 c -2.209 0 -4 1.791 -4 4 s 1.791 4 4 4 h 13.869 c 2.209 0 4 -1.791 4 -4 S 54.144 60.03 51.935 60.03 z" style="stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(255,255,255); fill-rule: nonzero; opacity: 1;" transform=" matrix(1 0 0 1 0 0) " stroke-linecap="round" />
                  <path d="M 69.718 23.879 H 20.282 c -2.209 0 -4 1.791 -4 4 s 1.791 4 4 4 h 49.436 c 2.209 0 4 -1.791 4 -4 S 71.927 23.879 69.718 23.879 z" style="stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(255,255,255); fill-rule: nonzero; opacity: 1;" transform=" matrix(1 0 0 1 0 0) " stroke-linecap="round" />
                  <path d="M 60.826 41.955 H 29.174 c -2.209 0 -4 1.791 -4 4 c 0 2.209 1.791 4 4 4 h 31.652 c 2.209 0 4 -1.791 4 -4 C 64.826 43.746 63.035 41.955 60.826 41.955 z" style="stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(255,255,255); fill-rule: nonzero; opacity: 1;" transform=" matrix(1 0 0 1 0 0) " stroke-linecap="round" />
                </g>
                </g>
                </svg>
              </span>
            </div>
          </th>
                    <th style="background-color:rgb(4, 220, 4)">
					<label class="form-checkbox">
    <input type="checkbox" v-model="selectAll" @click="select">
    <i class="form-icon"></i>
  </label>
				</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="td in tableData" :key="td.link" >
          <td @click="show=true, description=td.descriptionNER, 
          getObjectforHighlight(td.link)"
          title="Click to see course description">{{ td.crs_name }}</td>
          <td>{{ td.type }}</td>
          <td>{{ td.skill_name }}</td>
          <td>
            <span v-bind:class="td.score >= 0.9 ? 'score high' : td.score >= 0.75 ? 'score mid' : 'score low'">{{ td.score }}</span>
          </td>
          <td>
            <label class="form-checkbox">
                <input type="checkbox" :value="td" v-model="selected">
              <i class="form-icon"></i>
              </label>
          </td>
        </tr>
      </tbody>
    </table>
    <div class="table-footer">
      <div class="start:flex-items">Show {{ showInfo.from }} to {{ showInfo.to }} of {{ showInfo.of }} entries</div>
      <div class="end:flex center:items">
        <ul class="pagination:nav">
          <li :class="['nav-item', { 'disabled': currentPage === 1 }]">
            <a href="#" class="nav-link" @click.prevent="currentPage = 1, paginateEntries()">First</a>
          </li>
          <li :class="['nav-item', { 'disabled': currentPage === 1 }]">
            <a href="#" class="nav-link" @click.prevent="(currentPage < 1) ? currentPage = 1 : currentPage -= 1, paginateEntries()">Prev</a>
          </li>
          <li v-for="pagi in showPagination" :key="pagi" :class="['nav-item', {'ellipsis': pagi === '...', 'active': pagi === currentPage}]">
            <a href="#" class="nav-link" @click.prevent="paginateEvent(pagi)">{{ pagi }}</a>
          </li>
          <li :class="['nav-item', { 'disabled': currentPage === allPages }]">
            <a href="#" class="nav-link" @click.prevent="(currentPage > allPages) ? currentPage = allPages : currentPage += 1, paginateEntries()">Next</a>
          </li>
          <li :class="['nav-item', { 'disabled': currentPage === allPages }]">
            <a href="#" class="nav-link" @click.prevent="currentPage = allPages, paginateEntries()">Last</a>
          </li>
        </ul>
      </div>
    </div>
    <b-button variant="success" style="display: block;margin-left:auto; margin-right:auto" v-on:click="ApproveObjectNer">Next</b-button>
    <a-modal v-model="show" title="Course Description" style="margin-top: 180px;" class="course-description"
    :ok-button-props="{ style: { display: 'none' } }">
      <text-highlight :queries="queries">{{ description }}</text-highlight>
    </a-modal>
  </div>
</template>

<script>
import { $array, $object } from 'alga-js/dist/alga.min.js'
import axios from 'axios';
import Treeselect from '@riophae/vue-treeselect'
import TextHighlight from 'vue-text-highlight';
export default {
  name: 'NER',
  data() {
    return {
      queries: [],
      dropdown: false,
      dropdown1: false,
       selectAll: false,
      show: false,
      selected: [],
      description: '',
      columns: [
        { name: 'crs_name', text: 'Course Name', disable: false  },
        { name: 'link', text: 'Link Course', disable: true  },
        { name: 'descriptionNER', text: 'Description', disable: true },
        { name: 'type', text: 'Type', disable: false  },
        { name: 'skill_name', text: 'Skill Name', disable: false  },
        { name: 'score', text: 'Score', disable: false  },
      ],
      RangeScore: [
      { id: 0.9, label: '>= 90%' },
      { id: 0.8, label: '>= 80%' },
      { id: 0.75, label: '>= 75%' },
      { id: 0.7, label: '>= 70%' }
      ],
      SkillType: [
      { id: 'Knowledge', label: 'Knowledge' },
      { id: 'Programming Language', label: 'Programming Language' },
      { id: 'Framework', label: 'Framework' },
      { id: 'Platform', label: 'Platform' },
      { id: 'Tool', label: 'Tool' },
      { id: 'Task', label: 'Task' },
      { id: 'Softskill', label: 'Softskill' },
      ],
      entries: [],
      showEntries: [5, 10, 15, 25, 50, 75, 100],
      currentEntries: 5,
      filteredEntries: [],
      filterData: [],
      currentPage: 1,
      allPages: 1,
      searchInput: '',
      searchEntries: [],
      outputname: '',
      index: 0,
      col: {
        crs_name: '',
        type:'',
        skill_name: '',
        score: ''
      },
      sortcol: {
        crs_name: '',
        type:'',
        skill_name: '',
        score: ''
      }
    }
  },
  components: { TextHighlight, Treeselect },
  computed: {
    showInfo() {
      return $array.show(this.getCurrentEntries(),this.currentPage, this.currentEntries)
    },
    showPagination() {
      return $array.pagination(this.allPages, this.currentPage, 3)
    },
    tableHeader() {
      return this.columns.filter(i => i.disable === false)
    },
    tableData() {
      return this.filteredEntries
    },
    pageSalaries() {
      return $array.sum(this.filteredEntries, 'salary')
    },
    totalSalaries() {
      return $array.sum(this.entries, 'salary')
    }
  },
  created() {
    this.outputname = this.$route.params.train_output;
    axios.post(`api/get_result_train/`, {input_path: this.outputname})
    .then(response => {
      this.entries = JSON.parse(response.data)
      console.log(this.entries)
      this.paginateData(this.entries)
    })
    .catch(e => {
      this.errors.push(e)
    })
  },
  methods: {
    async ApproveObjectNer() {
      await axios
        .post(`api/insert_course_skill/`, {
          input_path: this.outputname,
          skill: this.selected,
          }
        )
        .then(() => {
          alert("Insert data into Neo4j success!")
          this.$router.push({
            name: 'Dashboard',
          });
        })
        .catch((err) => {
          console.log(err);
          alert("Insert data into Neo4j fail!")
        });
    },
    paginateEntries() {
      if(this.searchInput.length >= 3) {
        this.searchEntries = $array.search(this.entries,this.searchInput)
        console.log(this.searchEntries)
        this.paginateData(this.searchEntries)
        this.allPages = $array.pages(this.searchEntries, this.currentEntries)
      } else {
        this.searchEntries = []
        this.paginateData(this.entries)
        this.allPages = $array.pages(this.entries, this.currentEntries)
      }
    },
    paginateEvent(page) {
      this.currentPage = page
      this.paginateEntries()
    },
    searchEvent() {
      this.currentPage = 1
      this.paginateEntries()
    },
    paginateData(data) {
      this.filteredEntries = $array.paginate(data, this.currentPage, this.currentEntries)
      this.allPages = $array.pages(data, this.currentEntries)
    },
    getCurrentEntries() {
      return (this.searchEntries.length <= 0) ? this.entries : this.searchEntries
    },
    filterByColumn() {
      const filterCol = $object.removeBy('')(this.col)
      let filterData = this.getCurrentEntries()
      if(Object.entries(filterCol).length >= 1) {
        filterData = $array.filtered(...Object.values(filterCol))(this.getCurrentEntries(), Object.keys(filterCol))
      }
      this.paginateData(filterData)
    },
    sortByColumn(column) {
      this.col = {
        crs_name: '',
        type: '',
        skill_name: '',
        score: 0
      }
      let sortedEntries = this.getCurrentEntries()
      const sortedColumn = this.sortcol[column]
      if(sortedColumn === '') {
        this.sortcol[column] = 'asc'
        sortedEntries = $array.sorted(this.getCurrentEntries(),column, 'asc')
      } else if(sortedColumn === 'asc') {
        this.sortcol[column] = 'desc'
        sortedEntries = $array.sorted(this.getCurrentEntries(),column, 'desc')
      } else if(sortedColumn === 'desc') {
        this.sortcol[column] = ''
      }
      this.paginateData(sortedEntries)
    },
    select() {
			this.selected = [];
			if (!this.selectAll) {
				for (let i in this.entries) {
					this.selected.push(this.entries[i]);
				}
			}
      console.log(this.selected)
		},
    ChooseRangeScore(){
      this.selected = [];
      for (let i in this.entries) {
          if(this.entries[i].score >= this.valueScore){
            console.log(this.entries[i].score, this.value)
            console.log("vaoday choose if")
            this.selected.push(this.entries[i]);
          }
				}
    },
    changeShow(type){
      if(type === 'Score'){
        this.dropdown = !this.dropdown
      }
      if(type === 'Type'){
        this.dropdown1 = !this.dropdown1
      }
    },
    filterColumn(){
      this.filterData = []
      let filterData = [] 
      let skilltype = false
      if(this.valueSkillType != null){
        if(this.valueSkillType.length != 0){
          skilltype = true
        }
      }
      if(skilltype == true){
        for(let i in this.valueSkillType){
          for (let j in this.entries) {
            if(this.entries[j].type === this.valueSkillType[i]){
              this.filterData.push(this.entries[j]);
            }
          }
        }
      }
      else{
        this.filterData = this.entries
      }
      console.log(this.filterData)
      if(this.valueRangeScore != null & skilltype == true){
        console.log("vao for score khi co filter type")
        for(let i in this.filterData){
          if(this.filterData[i].score >= this.valueRangeScore){
            filterData.push(this.filterData[i]);
          }
        }
      }
      else if(this.valueRangeScore != null){
        console.log("vao for score")
        for(let i in this.entries){
          if(this.entries[i].score >= this.valueRangeScore){
            filterData.push(this.entries[i]);
          }
        }
      }

      console.log(filterData)
      if(filterData.length != 0 | this.valueRangeScore != null){
        this.paginateData(filterData)
      }
      else{
        this.paginateData(this.filterData)
      }
    },
    getObjectforHighlight(link){
      let filterData = []
      this.queries = []
      filterData = $array.filtered(this.entries, {'link':link})
      for (let i in filterData) {
        this.queries.push(filterData[i].skill_name + '(' + (filterData[i].type).toUpperCase() + ')')
			}
      console.log(filterData)
    },
  }
}
</script>

<style lang='scss'>
.course-description .ant-modal {
  width: 68% !important
}
.header-filter {
  display: flex;
  flex-wrap: wrap;
}
.container{
  width: 100%;
  font-family: 'Lato', sans-serif;
  margin-top: 10px;
}
.score {
    display: inline-block;
    line-height: 30px;
    font-size: 14px;
    color: #fff;
    padding: 0 15px;
    -webkit-border-radius: 3px;
    -moz-border-radius: 3px;
    border-radius: 3px;
    text-transform: capitalize;
}

.score.low {
    background: #fa4251;
}

.score.mid {
    background: #00b5e9;
}

.score.high {
    background: #57b846;
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
.tableheader {
  display: flex;
  flex-wrap: wrap;
  flex-direction: row;
}
.tableheader > div {
  display: flex;
  flex-direction: row;
  align-items: center;
  margin-left: 5px;
}
.table-footer {
  display: flex !important;
  justify-content: space-between;
    div {
      margin-top: 5px;
      font-weight: 700;

    }
  div ul{

    display: flex !important;
    list-style-type: none;
    li a {
      color: rgb(2, 150, 2);
      // border: 2px solid rgb(175, 175, 175) !important;
      // margin-left: -1px;
      font-weight: 600;
      text-decoration: underline;
    }
    a:hover {
      color: white;
      border-radius: 5px;
      background-color: rgb(2, 150, 2);
      text-decoration: none;
    }
  }
}
.table {
  margin-bottom: 0px !important;
}
tr:hover{background-color:rgb(230, 243, 231);cursor:pointer;}

.select-css {
	display: block;
	font-size: 13px;
	font-family: sans-serif;
	font-weight: 700;
	color: rgb(97, 95, 95);
	line-height: 1.0;
	padding: .6em 1.4em .5em .8em;
	width: 55px;
	max-width: 55px; 
	box-sizing: border-box;
	margin: 0;
  margin-left: 5px;
  margin-right: 5px;
	border: 1px solid #aaa;
	box-shadow: 0 1px 0 1px rgba(0,0,0,.04);
	border-radius: .5em;
	-moz-appearance: none;
	-webkit-appearance: none;
	appearance: none;
	background-color: #fff;
	background-image: url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%23007CB2%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E'), linear-gradient(to bottom, #ffffff 0%,#e5e5e5 100%);
	background-repeat: no-repeat, repeat;
	background-position: right .7em top 50%, 0 0;
	background-size: .65em auto, 100%;
}
.select-css::-ms-expand {
	display: none;
}
.select-css:hover {
	border-color: #888;
}
.select-css:focus {
	border-color: #aaa;
	color: #222; 
	outline: none;
}
.select-css option {
	font-weight:normal;
}
</style>