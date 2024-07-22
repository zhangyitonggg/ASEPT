
<template>
  <v-container fluid>
    <v-col>
      <v-list three-line>
        <template v-for="(item, index) in items">
          <v-subheader
            v-if="item.header"
            :key="item.header"
            v-text="item.header"
          ></v-subheader>
          <v-divider
            v-else-if="item.divider"
            :key="index"
            :inset="item.inset"
          ></v-divider>
          <v-list-item
            v-else-if="item.name"
            :key="item.name"
          >
            <v-list-item-avatar>
              <v-icon> {{ item.locked ? "mdi-link-lock" : "mdi-link" }}</v-icon>
            </v-list-item-avatar>
            <v-list-item-content>
              <v-list-item-title>
                <h4>
                  {{ item.name }}
                </h4>
              </v-list-item-title>
              <v-list-item-subtitle>
                Tag: {{ item.tag }}
              </v-list-item-subtitle>
            </v-list-item-content>
            <v-list-item-action>
              <v-btn
                color="primary"
                @click="addToList(item)"
              > 加入题单 </v-btn>
            </v-list-item-action>
            <v-list-item-action>
              <v-btn
                color="primary"
                @click="changeProblem(item)"
              > 修改问题 </v-btn>
            </v-list-item-action>
          </v-list-item>
        </template>
      </v-list>
      <v-btn
        color="primary"
        @click="dialogCreate = true"
        class="mt-4"
      >
        创建题目
      </v-btn>
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
          <v-text-field
            v-model="newProblem.name"
            label="题目名称"
            required
          ></v-text-field>
          <v-textarea
            v-model="newProblem.content"
            label="题目内容"
            rows="4"
            required
          ></v-textarea>
          <v-text-field
            v-model="newProblem.tag"
            label="标签"
          ></v-text-field>
          <v-select
            v-model="newProblem.type"
            :items="questionTypes"
            label="题目类型"
            required
          ></v-select>
          <template v-if="isMultipleChoice(newProblem.type)">
            <v-text-field
              v-for="(option, index) in newProblem.options"
              :key="index"
              :label="'选项 ' + (index + 1)"
              v-model="newProblem.options[index]"
            >
              <template v-slot:append>
                <v-btn icon @click="removeOption(index)">
                  <v-icon>mdi-close</v-icon>
                </v-btn>
              </template>
            </v-text-field>
            <v-btn @click="addOption">添加选项</v-btn>
          </template>
          <template v-if="newProblem.type === 'FILL_BLANK'">
            <v-text-field
              v-for="(blank, index) in newProblem.fillBlanks"
              :key="index"
              :label="'填空答案 ' + (index + 1)"
              v-model="newProblem.fillBlanks[index]"
            ></v-text-field>
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
          <v-select
            v-model="selectedList"
            :items="listOptions"
            label="选择题单"
            item-text="name"
            item-value="id"
            required
          ></v-select>
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
          <v-text-field
            v-model="currentProblem.name"
            label="题目名称"
            required
          ></v-text-field>
          <v-textarea
            v-model="currentProblem.content"
            label="题目内容"
            rows="4"
            required
          ></v-textarea>
          <!-- 可以添加其他题目信息的输入框 -->
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="confirmChangeProblem">保存修改</v-btn>
          <v-btn text @click="dialogEdit = false">取消</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
export default {
  data () {
    return {
      dialogCreate: false, // 控制“创建题目”对话框的显示
      dialogAdd: false, // 控制“添加题单”对话框的显示
      dialogEdit: false, // 控制“修改问题”对话框的显示
      currentProblem: {}, // 当前正在修改的题目
      newProblem: { name: '', content: '', tag: '', type: '', options: [''], fillBlanks: [''] }, // 新创建的题目
      selectedList: null, // 选择的题单ID
      listOptions: [ // 题单选项
        { id: 'list1', name: '题单1' },
        { id: 'list2', name: '题单2' },
        // 更多题单选项
      ],
      questionTypes: [ // 题目类型选项
        { text: '单选', value: 'SINGLE_CHOICE' },
        { text: '多选', value: 'MULTIPLE_CHOICE' },
        { text: '填空', value: 'FILL_BLANK' },
      ],
      itemsPerPageArray: [4, 8, 12],
      search: '',
      filter: {},
      sortDesc: false,
      page: 1,
      itemsPerPage: 4,
      sortBy: 'name',
      keys: [
        'Name',
        'Tag',
      ],
      items: [
        { header: '我创建的题目' },
        {
          name: 'Problem1',
          tag: 'Descrlines.',
          gid: 'xxx1',
          locked: true,
          content: '66666666',
        },
        {
          name: 'Group2',
          tag: 'Descrlines.',
          gid: 'xxx2',
          locked: true,
        },
        {
          name: 'Group3',
          founder: 'User3',
          description: 'Descrlines.',
          gid: 'xxx3',
          locked: false,
        },
      ],
    }
  },
  computed: {
    numberOfPages () {
      return Math.ceil(this.items.length / this.itemsPerPage)
    },
    filteredKeys () {
      return this.keys.filter(key => key !== 'Name')
    },
  },
  methods: {
    isMultipleChoice(type) {
      return ['SINGLE_CHOICE', 'MULTIPLE_CHOICE'].includes(type);
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
    createProblem() {
      if (this.newProblem.name && this.newProblem.content) {
        this.items.push({ ...this.newProblem, gid: Date.now().toString() }); // 添加新题目
        this.newProblem = { name: '', content: '', tag: '', type: '', options: [''], fillBlanks: [''] }; // 重置表单
        this.dialogCreate = false; // 关闭对话框
      } else {
        alert('请填写题目名称和内容！');
      }
    },
    changeProblem(item) {
      this.currentProblem = { ...item }; // 复制题目以进行编辑
      this.dialogEdit = true;
    },
    addToList(item) {
      this.currentProblem = item; // 记录当前题目
      this.dialogAdd = true;
    },
    confirmAddToList() {
      alert(`题目 ${this.currentProblem.name} 已添加到题单 ${this.selectedList}`);
      // 在这里添加将题目加入题单的逻辑
      this.dialogAdd = false;
    },
    confirmChangeProblem() {
      alert(`题目 ${this.currentProblem.name} 已保存修改`);
      // 在这里添加保存题目修改的逻辑
      this.dialogEdit = false;
    }
  },
}
</script>

<style scoped>
.scrollable-container {
  position: relative;
  top: -10%;
  height: 100%;
  overflow: auto;
}

.header-title {
  font-size: 18px;
  font-weight: 500;
  color: #ffffff;
  margin-right: 30%;
}

.pagination-info {
  font-size: 16px;
  font-weight: bold;
  margin-left: 2%; /* Adjust as needed to move it slightly to the right */
}

.item-card {
  display: flex;
  flex-direction: column;
  height: 100%;
  position: relative;
}

.description-text {
  display: block;
  white-space: normal; /* Allow text to wrap onto multiple lines */
}

.apply-button {
  font-size: 14px;
  position: absolute;
  color: white;
  font-weight:900;
  top: 15px;
  right: 20px;
}
</style>