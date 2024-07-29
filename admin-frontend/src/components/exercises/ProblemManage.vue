<template>
  <div>
    <template v-if="loading">
      <v-container fluid class="d-flex align-center justify-center">
        <v-row class="text-center">
          <v-col>
            <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
          </v-col>
        </v-row>
      </v-container>
      <v-container fluid class="d-flex align-center justify-center">
        <v-row class="text-center">
          <v-col>
            <h3>
              落霞与孤鹜齐飞，秋水共长天一色。
            </h3>
            <span>正在获取你管理的题目。</span>
          </v-col>
        </v-row>
      </v-container>
    </template>
    <v-container fluid v-else>
      <v-layout>
        <v-flex xs1>
          <v-btn color="primary" @click="openCreateDialog">创建题目</v-btn>
        </v-flex>
        <v-spacer />
        <v-flex xs24>
          <searchbar v-model="search" searchBtnText='搜索题目' />
        </v-flex>
      </v-layout>
      <v-col>
        <v-list three-line>
          <template v-for="(item, index) in currentPageItems">
            <v-subheader v-if="item.header" :key="item.header" v-text="item.header"></v-subheader>
            <v-divider v-else-if="item.divider" :key="index" :inset="item.inset"></v-divider>
            <v-list-item v-else-if="item.title" :key="item.pid">
              <v-list-item-avatar>
                <v-icon> mdi-help-circle-outline</v-icon>
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title>
                  <h4>{{ item.title }}</h4>
                </v-list-item-title>
                <v-list-item-subtitle>Tag: {{ item.tagsString }}</v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action>
                <v-btn class="butspace" color="primary" @click="openAddTagDialog(item)">增加 Tag</v-btn>
              </v-list-item-action>
              <v-list-item-action>
                <v-btn color="primary" @click="addToList(item)">加入题单</v-btn>
              </v-list-item-action>
              <v-list-item-action>
                <v-btn class="butspace" color="primary" @click="changeProblem(item)">修改问题</v-btn>
              </v-list-item-action>
            </v-list-item>
            <v-divider v-if="index < currentPageItems.length - 1"></v-divider>
          </template>
          <v-pagination v-model="currentPage" :length="numberOfPages"></v-pagination>
        </v-list>
      </v-col>
      <!-- 创建题目对话框 -->
      <v-dialog v-model="dialogCreate" fullscreen hide-overlay scrollable transition="dialog-bottom-transition">
        <v-card>
          <v-card-title>
            <h3>
              创建新题目
            </h3>
            <v-spacer></v-spacer>
            <v-btn icon @click="dialogCreate = false">
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-card-title>
          <v-card-text>
            <v-stepper v-model="e1">
              <v-stepper-header>
                <v-stepper-step :complete="e1 > 1" step="1"> 从 PDF 或图像提取文字
                </v-stepper-step>
                <v-divider></v-divider>
                <v-stepper-step :complete="e1 > 2" step="2"> 完善题目信息
                </v-stepper-step>
                <v-divider></v-divider>
                <v-stepper-step step="3">
                  预览并保存
                </v-stepper-step>
              </v-stepper-header>
              <v-stepper-items>
                <v-stepper-content step="1">
                  <v-file-input v-model="uploadedFile" accept=".pdf, .jpg, .jpeg, .png"
                    label="选择 PDF 或图像文件"></v-file-input>
                  <v-btn color="primary" @click="handleFileUpload" block
                    :disabled="loading_file_convert || !uploadedFile" class="mb-4"> 提取文本 </v-btn>
                  <v-textarea v-model="newProblem.content" label="提取的文本" rows="20" hint="支持 Markdown 语法" required
                    :disabled="!newProblem.content" :loading="loading_file_convert"></v-textarea>
                  <v-banner v-if="loading_file_convert" color="info"> 我们正在为你提取文件里的文本。这可能需要一些时间。 </v-banner>
                  <v-banner v-else-if="newProblem.content" color="warning"> 提取的文字可能有错误。请手动修正。 </v-banner>
                </v-stepper-content>
                <v-stepper-content step="2">
                  <v-text-field v-model="newProblem.name" label="题目名称" required></v-text-field>
                  <v-textarea v-model="newProblem.content" label="题目内容" rows="23" required
                    hint="支持 Markdown 语法"></v-textarea>
                  <v-select v-model="newProblem.type" :items="questionTypes" label="题目类型" required></v-select>
                  <template v-if="isMultipleChoice(newProblem.type)">
                    <v-text-field v-for="(option, index) in newProblem.options" :key="index"
                      :label="'选项 ' + (index + 1)" v-model="newProblem.options[index]">
                      <template v-slot:append>
                        <v-btn icon @click="removeOption(index)">
                          <v-icon>mdi-close</v-icon>
                        </v-btn>
                      </template>
                    </v-text-field>
                    <v-select v-if="newProblem.type === 'SINGLE_CHOICE'" v-model="newProblem.correctAnswer"
                      :items="newProblem.options.map((opt, index) => ({ text: opt, value: String.fromCharCode(65 + index) }))"
                      label="选择正确答案" required></v-select>
                    <v-select v-if="newProblem.type === 'MULTI_CHOICE'" v-model="newProblem.correctAnswers"
                      :items="newProblem.options.map((opt, index) => ({ text: opt, value: String.fromCharCode(65 + index) }))"
                      label="选择正确答案" multiple required></v-select>
                    <v-btn @click="addOption">添加选项</v-btn>
                  </template>
                  <template v-if="newProblem.type === 'BLANK_FILLING'">
                    <v-text-field v-for="(blank, index) in newProblem.fillBlanks" :key="index"
                      :label="'填空答案 ' + (index + 1)" v-model="newProblem.fillBlanks[index]"></v-text-field>
                    <v-btn @click="addFillBlank">添加答案</v-btn>
                  </template>
                </v-stepper-content>
                <v-stepper-content step="3">
                  <v-text-field v-model="newProblem.name" label="题目名称" required disabled></v-text-field>
                  <v-subheader>题目内容</v-subheader>
                  <v-md-preview :text="newProblem.content"></v-md-preview>
                  <v-select v-model="newProblem.type" :items="questionTypes" label="题目类型" required disabled></v-select>
                  <template v-if="isMultipleChoice(newProblem.type)">
                    <v-text-field v-for="(option, index) in newProblem.options" :key="index"
                      :label="'选项 ' + (index + 1)" v-model="newProblem.options[index]" disabled>
                      <template v-slot:append>
                        <v-btn icon @click="removeOption(index)" disabled>
                          <v-icon>mdi-close</v-icon>
                        </v-btn>
                      </template>
                    </v-text-field>
                    <v-select disabled v-if="newProblem.type === 'SINGLE_CHOICE'" v-model="newProblem.correctAnswer"
                      :items="newProblem.options.map((opt, index) => ({ text: opt, value: String.fromCharCode(65 + index) }))"
                      label="选择正确答案" required></v-select>
                    <v-select disabled v-if="newProblem.type === 'MULTI_CHOICE'" v-model="newProblem.correctAnswers"
                      :items="newProblem.options.map((opt, index) => ({ text: opt, value: String.fromCharCode(65 + index) }))"
                      label="选择正确答案" multiple required></v-select>
                  </template>
                  <template v-if="newProblem.type === 'BLANK_FILLING'">
                    <v-text-field disabled v-for="(blank, index) in newProblem.fillBlanks" :key="index"
                      :label="'填空答案 ' + (index + 1)" v-model="newProblem.fillBlanks[index]"></v-text-field>
                  </template>
                </v-stepper-content>
              </v-stepper-items>
            </v-stepper>
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn @click="e1 = e1 - 1" :disabled="e1 == 1" large> 上一步 </v-btn>
            <v-btn color="primary" @click="createProblem" large> {{ `${e1 != 3 ? "下一步" : "保存"}` }} </v-btn>
            <v-btn color="error" outlined @click="dialogCreate = false" large> 取消 </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-dialog v-model="dialogAdd" max-width="50%">
        <v-card>
          <v-card-title>
            添加题目到题单
            <v-spacer></v-spacer>
            <v-btn icon @click="dialogAdd = false">
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-card-title>
          <v-card-text>
            请选择要添加到的题单:
            <v-select v-model="selectedList" :items="listOptions" label="选择题单" item-text="name" item-value="pgid"
              required></v-select>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="confirmAddToList">确认添加</v-btn>
            <v-btn text @click="dialogAdd = false">取消</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <!-- 修改题目对话框 -->
      <v-dialog v-model="dialogEdit" fullscreen hide-overlay scrollable transition="dialog-bottom-transition">
        <v-card>
          <v-card-title>
            <h3>
              修改题目
            </h3>
            <v-spacer></v-spacer>
            <v-btn icon @click="dialogEdit = false">
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-card-title>
          <v-card-text>
            <v-stepper v-model="e2">
              <v-stepper-header>
                <v-stepper-step :complete="e2 > 1" step="1"> 修改题目信息
                </v-stepper-step>
                <v-divider></v-divider>
                <v-stepper-step :complete="e1 > 2" step="2"> 预览并保存
                </v-stepper-step>
              </v-stepper-header>
              <v-stepper-items>
                <v-stepper-content step="1">
                  <v-text-field v-model="currentProblem.title" label="题目名称" required></v-text-field>
                  <v-textarea v-model="currentProblem.content" label="题目内容" rows="23" required
                    hint="支持 Markdown 语法"></v-textarea>
                  <v-select v-model="currentProblem.type" :items="questionTypes" label="题目类型" required></v-select>
                  <template v-if="isMultipleChoice(currentProblem.type)">
                    <v-text-field v-for="(option, index) in currentProblem.choices" :key="index"
                      :label="'选项 ' + (index + 1)" v-model="currentProblem.choices[index]">
                      <template v-slot:append>
                        <v-btn icon @click="removeCurOption(index)">
                          <v-icon>mdi-close</v-icon>
                        </v-btn>
                      </template>
                    </v-text-field>
                    <v-select v-if="currentProblem.type === 'SINGLE_CHOICE'" 
                      v-model="currentProblem.answers" 
                      :items="parsedChoices" 
                      item-text="text" 
                      item-value="value" 
                      label="选择正确答案" 
                      required>
                    </v-select>
                    <v-select v-if="currentProblem.type === 'MULTI_CHOICE'" 
                      v-model="currentProblem.answers" 
                      :items="parsedChoices" 
                      item-text="text" 
                      item-value="value" 
                      label="选择正确答案" 
                      multiple 
                      required>
                    </v-select>
                    <v-btn @click="addOption">添加选项</v-btn>
                  </template>
                  <template v-if="currentProblem.type === 'BLANK_FILLING'">
                    <v-text-field v-for="(blank, index) in currentProblem.fillBlanks" :key="index"
                      :label="'填空答案 ' + (index + 1)" v-model="currentProblem.fillBlanks[index]"></v-text-field>
                    <v-btn @click="addFillBlank">添加答案</v-btn>
                  </template>
                </v-stepper-content>
                <v-stepper-content step="2">
                  <v-text-field v-model="currentProblem.title" label="题目名称" required disabled></v-text-field>
                  <v-subheader>题目内容</v-subheader>
                  <v-md-preview :text="currentProblem.content"></v-md-preview>
                  <v-select v-model="currentProblem.type" :items="questionTypes" label="题目类型" required
                    disabled></v-select>
                  <template v-if="isMultipleChoice(currentProblem.type)">
                    <v-text-field v-for="(option, index) in currentProblem.options" :key="index"
                      :label="'选项 ' + (index + 1)" v-model="currentProblem.options[index]" disabled>
                      <template v-slot:append>
                        <v-btn icon @click="removeCurOption(index)" disabled>
                          <v-icon>mdi-close</v-icon>
                        </v-btn>
                      </template>
                    </v-text-field>
                    <v-select disabled v-if="currentProblem.type === 'SINGLE_CHOICE'"
                      v-model="currentProblem.correctAnswer"
                      :items="parsedOptions"
                      label="选择正确答案" required></v-select>
                    <v-select disabled v-if="currentProblem.type === 'MULTI_CHOICE'"
                      v-model="currentProblem.correctAnswers"
                      :items="parsedOptions"
                      label="选择正确答案" multiple required></v-select>
                  </template>
                  <template v-if="currentProblem.type === 'BLANK_FILLING'">
                    <v-text-field disabled v-for="(blank, index) in currentProblem.fillBlanks" :key="index"
                      :label="'填空答案 ' + (index + 1)" v-model="currentProblem.fillBlanks[index]"></v-text-field>
                  </template>
                </v-stepper-content>
              </v-stepper-items>
            </v-stepper>
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn @click="e2 = e2 - 1" large :disabled="e2 == 1"> 上一步 </v-btn>
            <v-btn color="primary" @click="confirmChangeProblem" large> {{ `${this.e2 == 1 ? "下一步" : "保存修改"}` }}</v-btn>
            <v-btn text @click="dialogEdit = false" large outlined color="error">取消</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <!-- 增加Tag对话框 -->
      <v-dialog v-model="dialogAddTag" max-width="600px">
        <v-card>
          <v-card-title>
            增加 Tag
            <v-spacer></v-spacer>
            <v-btn icon @click="dialogAddTag = false">
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-card-title>
          <v-card-text>
            <v-text-field v-model="newTag" label="输入 Tag" required></v-text-field>
            <!-- 可选 Tag 显示区域 -->
            <v-chip-group column v-model="selectedTags" multiple active-class="primary--text">
              <v-chip v-for="tag in availableTags" :key="tag.tid" @click="newTag = tag.tag_name" color="yellow"
                text-color="white">
                {{ tag.tag_name }}
              </v-chip>
            </v-chip-group>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="confirmAddTag">确认增加</v-btn>
            <v-btn text @click="dialogAddTag = false">取消</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
  </div>
</template>

<script>
import searchbar from '../SearchBar.vue';

import VMdPreview from '@kangc/v-md-editor/lib/preview';
import '@kangc/v-md-editor/lib/style/preview.css';
import githubTheme from '@kangc/v-md-editor/lib/theme/github.js';
import '@kangc/v-md-editor/lib/theme/style/github.css';
import hljs from 'highlight.js';

VMdPreview.use(githubTheme, {
  Hljs: hljs,
});

export default {
  data() {
    return {
      e1: 1,
      e2: 1,
      loading_file_convert: false, // 控制文件转换的加载状态
      dialogCreate: false, // 控制“创建题目”对话框的显示
      dialogAdd: false, // 控制“添加题单”对话框的显示
      dialogEdit: false, // 控制“修改问题”对话框的显示
      dialogAddTag: false, // 控制“增加Tag”对话框的显示
      currentProblem: {}, // 当前正在修改的题目
      newProblem: { name: '', content: '', tag: '', type: '', options: [''], fillBlanks: [''] }, // 新创建的题目
      newTag: '', // 新的 Tag
      selectedList: null, // 选择的题单ID
      listOptions: [], // 题单选项，将从后端获取
      questionTypes: [ // 题目类型选项
        { text: '单选', value: 'SINGLE_CHOICE' },
        { text: '多选', value: 'MULTI_CHOICE' },
        { text: '填空', value: 'BLANK_FILLING' },
      ],
      loading: true,
      items: [
        { header: '我创建的题目' },
      ],
      itemsPerPage: 13,
      uploadedFile: null, // 上传的文件
      currentPage: 1,
      problems: [],
      search: '',
      selectedTags: [], // 选中的标签
      newTag: '', // 新输入的标签
      availableTags: [], // 可用的标签
    };
  },
  created() {
    this.fetchProblems();
    this.fetchQuestionLists();
  },
  computed: {  
  parsedChoices() {
    let choices = [];
    console.log("Raw choices:", this.currentProblem.choices);
    try {
      let choicesObj = JSON.parse(this.currentProblem.choices);
      console.log("Parsed choices object:", choicesObj);
      choices = Object.keys(choicesObj).map((key) => ({
        text: choicesObj[key],
        value: key
      }));
      console.log("Formatted choices array:", choices);
    } catch (error) {
      console.error('Failed to parse choices:', error);
    }
    return choices;
  },
    parsedOptions() {
      let options = [];
      try {
        let optionsObj = JSON.parse(this.currentProblem.options);
        options = Object.keys(optionsObj).map((key, index) => ({
          text: optionsObj[key],
          value: key
        }));
      } catch (error) {
        console.error('Failed to parse options:', error);
      }
      return options;
    },
    numberOfPages() {
      return Math.ceil(this.filteredItems.length / this.itemsPerPage);
    },
    filteredKeys() {
      return this.keys.filter((key) => key !== 'Name');
    },
    filteredItems() {
      const filtered = this.items.filter(item =>
        item.title && item.title.toLowerCase().includes(this.search.toLowerCase())
      );
      return filtered;
    },
    currentPageItems() {
      const startIndex = (this.currentPage - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.filteredItems.slice(startIndex, endIndex).map(item => {
        return {
          ...item,
          tagsString: item.tags.join(' '),
        };
      });
    },
  },
  watch: {
    search() {
      this.currentPage = 1;
    },
    numberOfPages(newVal) {
      if (this.currentPage > newVal) {
        this.currentPage = newVal;
      }
    }
  },
  components: {
    searchbar,
    VMdPreview,
  },
  methods: {
    openCreateDialog() {
      this.e1 = 1;
      this.newProblem = { name: '', content: '', tag: '', type: '', options: [''], fillBlanks: [''] };
      this.dialogCreate = true;
    },
    handleFileUpload() {
      if (this.uploadedFile) {
        this.loading_file_convert = true;
        this.$store.dispatch('uploadFile', this.uploadedFile)
          .then(response => {
            this.newProblem.content = response.text;
          })
          .catch(error => {
            this.$store.commit('setAlert', {
              type: 'error',
              message: error.message || '上传文件失败。',
            });
          })
          .finally(() => {
            this.loading_file_convert = false;
          });
      }
    },
    fetchProblems() {
      this.$store
        .dispatch('getMyProblem')
        .then((res) => {
          console.log("res",res);
          this.items.splice(0, this.items.length, ...res.problems); // 清空当前数组并插入新数据
        })
        .catch((error) => {
          this.$store.commit('setAlert', {
            type: 'error',
            message: error,
          });
        })
        .finally(() => {
          this.loading = false;
        });
    },
    fetchQuestionLists() {
      this.$store
        .dispatch('getProblemGroup')
        .then((res) => {
          console.log("res",res);
          this.listOptions = res.problem_groups;
        })
        .catch((error) => {
          this.$store.commit('setAlert', {
            type: 'error',
            message: error,
          });
        });
    },
    isMultipleChoice(type) {
      return ['SINGLE_CHOICE', 'MULTI_CHOICE'].includes(type);
    },
    addOption() {
      this.newProblem.options.push('');
    },
    removeOption(index) {
      if (this.newProblem.options.length > 1) {
        this.newProblem.options.splice(index, 1);
      }
    },
    removeCurOption(index) {
      if (this.currentProblem.options.length > 1) {
        this.currentProblem.options.splice(index, 1);
      }
    },
    addFillBlank() {
      this.newProblem.fillBlanks.push('');
    },
    addToList(item) {
      this.currentProblem = item;
      this.dialogAdd = true;
    },
    changeProblem(item) {
      this.e2 = 1;
      this.currentProblem = item;
      console.log("cur",this.currentProblem);
      this.dialogEdit = true;
    },
    openAddTagDialog(item) {
      this.currentProblem = item;
      this.dialogAddTag = true;
      this.fetchTags();
    },
    fetchTags() {
      this.$store
        .dispatch('getProblemTags')
        .then(res => {
          this.availableTags = res.tags;
        })
        .catch(error => {
          this.$store.commit('setAlert', {
            type: 'error',
            message: error,
          });
        });
    },
    confirmAddTag() {
      if (this.newTag.trim() === '') {
        this.$store.commit('setAlert', {
          type: 'error',
          message: 'Tag 不能为空！',
        });
        return;
      }

      this.$store
        .dispatch('addTagToProblem', {
          pid: this.currentProblem.pid,
          tag: this.newTag,
        })
        .then(() => {
          this.$store.commit('setAlert', {
            type: 'success',
            message: 'Tag 增加成功！',
          });
          this.dialogAddTag = false;
          this.fetchProblems(); // 刷新题目列表
        })
        .catch((error) => {
          this.$store.commit('setAlert', {
            type: 'error',
            message: error,
          });
        });
    },
    confirmAddToList() {
      let proid = this.currentProblem.pid;
      let listid = this.selectedList;
      this.$store
        .dispatch('addProblemToList', {
          pid: proid,
          pgid: listid,
        })
        .then(() => {
          this.$store.commit('setAlert', {
            type: 'success',
            message: '题目成功加入题单！',
          });
          this.selectedList = null;
          this.dialogAdd = false;
        })
        .catch((error) => {
          this.$store.commit('setAlert', {
            type: 'error',
            message: error,
          });
        });
    },
    createProblem() {
      if (this.e1 != 3) {
        this.e1++;
        return;
      }
      let choices = {};
      let answer = {};
      if (this.newProblem.type === 'SINGLE_CHOICE' || this.newProblem.type === 'MULTI_CHOICE') {
        // 构造 choices 对象
        choices = this.newProblem.options.reduce((acc, choice, index) => {
          const key = String.fromCharCode(65 + index); // 生成键名，如 'A', 'B', 'C' 等
          if (choice.trim()) {
            acc[key] = choice;
          }
          return acc;
        }, {});
        if (this.newProblem.type === 'MULTI_CHOICE') {
          const sortedCorrectAnswers = this.newProblem.correctAnswers.slice().sort(); // 排序
          answer = sortedCorrectAnswers.reduce((acc, key) => {
            if (choices[key]) {
              acc[key] = choices[key];
            }
            return acc;
          }, {});
        } else if (this.newProblem.type === 'SINGLE_CHOICE') {
          const correctAnswerKey = this.newProblem.correctAnswer;
          if (correctAnswerKey && choices[correctAnswerKey]) {
            answer[correctAnswerKey] = choices[correctAnswerKey];
          }
        }
      } else if (this.newProblem.type === 'BLANK_FILLING') {
        // 构造填空题答案对象
        answer = this.newProblem.fillBlanks.reduce((acc, blank, index) => {
          acc[`${index + 1}`] = blank;
          return acc;
        }, {});
      }
      const choicesJson = JSON.stringify(choices);
      const answerJson = JSON.stringify(answer);
      const newProblemDataChoice = {
        title: this.newProblem.name,
        type: this.newProblem.type,
        content: this.newProblem.content,
        choices: choicesJson,
        answer: answerJson,
        tag: this.newProblem.tag,
      };
      const newProblemDataBlankFilling = {
        title: this.newProblem.name,
        type: this.newProblem.type,
        content: this.newProblem.content,
        answer: answerJson,
        tag: this.newProblem.tag,
      };
      let newProblemData = {};
      if (this.newProblem.type === 'BLANK_FILLING') {
        newProblemData = newProblemDataBlankFilling;
      } else {
        newProblemData = newProblemDataChoice;
      }
      this.$store
        .dispatch('createProblem', newProblemData)
        .then(() => {
          this.$store.commit('setAlert', {
            type: 'success',
            message: '题目创建成功！',
          });
          this.dialogCreate = false;
          this.newProblem = { name: '', content: '', tag: '', type: '', options: [''], fillBlanks: [''] };
          this.fetchProblems(); // 刷新题目列表
        })
        .catch((error) => {
          this.$store.commit('setAlert', {
            type: 'error',
            message: error,
          });
        });
    },
    resetNewProblem() {
      this.newProblem = {
        name: '',
        content: '',
        tag: '',
        type: '',
        options: [''],
        fillBlanks: [''],
        correctAnswers: [],
      };
    },
    confirmChangeProblem() {
      if (this.e2 != 2) {
        this.e2++;
        return;
      }
      this.$store
        .dispatch('updateProblem', this.currentProblem)
        .then(() => {
          this.$store.commit('setAlert', {
            type: 'success',
            message: '题目修改成功！',
          });
          this.dialogEdit = false;
          this.fetchProblems(); // 重新获取题目列表
        })
        .catch((error) => {
          this.$store.commit('setAlert', {
            type: 'error',
            message: error,
          });
        });
    },
  },
};
</script>

<style scoped>
.butspace {
  margin-right: 18px;
  /* 或其他适当的间距 */
}
</style>