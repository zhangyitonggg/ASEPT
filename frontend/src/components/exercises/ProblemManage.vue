<template>
  <div>
    <v-container fluid class="d-flex justify-center align-center" v-if="loading">
      <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
    </v-container>
    <v-container fluid v-else>
      <v-layout>
        <v-flex xs1>
          <v-btn color="primary" @click="dialogCreate = true">创建题目</v-btn>
        </v-flex>
        <v-spacer/>
        <v-flex xs24>
          <searchbar v-model="search" searchBtnText='搜索题目'/>
        </v-flex>
      </v-layout>
      <v-col>
        <v-list three-line>
          <template v-for="(item, index) in currentPageItems">
            <v-subheader v-if="item.header" :key="item.header" v-text="item.header"></v-subheader>
            <v-divider v-else-if="item.divider" :key="index" :inset="item.inset"></v-divider>
            <v-list-item v-else-if="item.title" :key="item.pid">
              <v-list-item-avatar>
                <v-icon> {{ item.locked ? "mdi-link-lock" : "mdi-link" }}</v-icon>
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title>
                  <h4>{{ item.title }}</h4>
                </v-list-item-title>
                <v-list-item-subtitle>Tag: {{ item.tag }}</v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action>
                <v-btn color="primary" @click="openAddTagDialog(item)">增加 Tag</v-btn>
              </v-list-item-action>
              <v-list-item-action>
                <v-btn color="primary" @click="addToList(item)">加入题单</v-btn>
              </v-list-item-action>
              <v-list-item-action>
                <v-btn color="primary" @click="changeProblem(item)">修改问题</v-btn>
              </v-list-item-action>
            </v-list-item>
          </template>
          <v-pagination v-model="currentPage" :length="numberOfPages"></v-pagination>
        </v-list>
      </v-col>

      <!-- 创建题目对话框 -->
<v-dialog v-model="dialogCreate" max-width="600px">
  <v-card>
    <v-card-title>
      创建新题目
      <v-spacer></v-spacer>
      <v-btn icon @click="dialogCreate = false">
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </v-card-title>
    <v-card-text>
      <v-file-input
        v-model="uploadedFile"
        ref="fileInput"
        label="上传 PDF 文件"
        accept=".pdf"
        @change="handleFileUpload"
      ></v-file-input>
      <v-text-field v-model="newProblem.name" label="题目名称" required></v-text-field>
      <v-textarea v-model="newProblem.content" label="题目内容" rows="4" required></v-textarea>
      <v-text-field v-model="newProblem.tag" label="标签"></v-text-field>
      <v-select v-model="newProblem.type" :items="questionTypes" label="题目类型" required></v-select>

      <!-- 单选和多选题的选项输入 -->
      <template v-if="isMultipleChoice(newProblem.type)">
        <v-text-field v-for="(option, index) in newProblem.options" :key="index" :label="'选项 ' + (index + 1)" v-model="newProblem.options[index]">
          <template v-slot:append>
            <v-btn icon @click="removeOption(index)">
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </template>
        </v-text-field>

        <v-select v-if="newProblem.type === 'SINGLE_CHOICE'" v-model="newProblem.correctAnswer" :items="newProblem.options.map((opt, index) => ({ text: opt, value: String.fromCharCode(65 + index) }))" label="选择正确答案" required></v-select>

        <v-select v-if="newProblem.type === 'MULTI_CHOICE'" v-model="newProblem.correctAnswers" :items="newProblem.options.map((opt, index) => ({ text: opt, value: String.fromCharCode(65 + index) }))" label="选择正确答案" multiple required></v-select>

        <v-btn @click="addOption">添加选项</v-btn>
      </template>

      <!-- 填空题的答案输入 -->
      <template v-if="newProblem.type === 'BLANK_FILLING'">
        <v-text-field v-for="(blank, index) in newProblem.fillBlanks" :key="index" :label="'填空答案 ' + (index + 1)" v-model="newProblem.fillBlanks[index]"></v-text-field>
        <v-btn @click="addFillBlank">添加答案</v-btn>
      </template>
    </v-card-text>
    <v-card-actions>
      <v-btn color="primary" @click="createProblem">保存题目</v-btn>
      <v-btn text @click="dialogCreate = false">取消</v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>


      <!-- 添加题单对话框 -->
      <v-dialog v-model="dialogAdd" max-width="600px">
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
            <v-select v-model="selectedList" :items="listOptions" label="选择题单" item-text="name" item-value="pgid" required></v-select>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="confirmAddToList">确认添加</v-btn>
            <v-btn text @click="dialogAdd = false">取消</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <!-- 修改题目对话框 -->
      <v-dialog v-model="dialogEdit" max-width="600px">
        <v-card>
          <v-card-title>
            修改问题
            <v-spacer></v-spacer>
            <v-btn icon @click="dialogEdit = false">
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-card-title>
          <v-card-text>
            <v-text-field v-model="currentProblem.name" label="题目名称" required></v-text-field>
            <v-textarea v-model="currentProblem.content" label="题目内容" rows="4" required></v-textarea>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="confirmChangeProblem">保存修改</v-btn>
            <v-btn text @click="dialogEdit = false">取消</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <!-- 增加Tag对话框 -->
      <v-dialog v-model="dialogAddTag" max-width="400px">
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
export default {
  data() {
    return {
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
      search:'',
    };
  },
  created() {
    this.fetchProblems();
    this.fetchQuestionLists();
  },
  computed: {
    numberOfPages() {
      return Math.ceil(this.items.length / this.itemsPerPage);
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
      return this.filteredItems.slice(startIndex, endIndex);
    },
  },
  components: {
    searchbar,
  },
  methods: {
    
    handleFileUpload() {
    // const fileInput = this.$refs.fileInput;
    // if (!fileInput || !fileInput.files || fileInput.files.length === 0) {
    //   this.$store.commit('setAlert', {
    //     type: 'error',
    //     message: '无法获取上传的文件。',
    //   });
    //   return;
    // }

    if (this.uploadedFile) {
        const file = this.uploadedFile;
        const formData = new FormData();
        formData.append('file', file);
      console.log(this.uploadedFile);
      console.log(formData);

    this.$store
      .dispatch('uploadFile', formData)
      .then(response => {
        // 假设 response.data.text 是从 PDF 中提取的文本
        this.newProblem.content = response.data.text;
      })
      .catch(error => {
        this.$store.commit('setAlert', {
          type: 'error',
          message: error.message || '上传文件失败。',
        });
      });
    }
  },
    fetchProblems() {
      this.$store
        .dispatch('getMyProblem')
        .then((res) => {
          this.items.splice(0, this.items.length, { header: '我创建的题目' }, ...res.problems); // 清空当前数组并插入新数据
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
      return ['SINGLE_CHOICE','MULTI_CHOICE'].includes(type);
    },
    addOption() {
      this.newProblem.options.push('');
    },
    removeOption(index) {
      if (this.newProblem.options.length > 1) {
        this.newProblem.options.splice(index, 1);
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
      this.currentProblem = item;
      this.dialogEdit = true;
    },
    openAddTagDialog(item) {
      this.currentProblem = item;
      this.dialogAddTag = true;
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

    // 将 correctAnswers 数组转为对象
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

  // 将对象转换为 JSON 字符串
  const choicesJson = JSON.stringify(choices);
  const answerJson = JSON.stringify(answer);

  // 准备新的题目数据
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
  if(this.newProblem.type === 'BLANK_FILLING') {
    newProblemData = newProblemDataBlankFilling;
  } else {
    newProblemData = newProblemDataChoice;
  }

  console.log(newProblemData);
  // 发送请求创建题目
  this.$store
    .dispatch('createProblem', newProblemData)
    .then(() => {
      this.$store.commit('setAlert', {
        type: 'success',
        message: '题目创建成功！',
      });
      this.dialogCreate = false;
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