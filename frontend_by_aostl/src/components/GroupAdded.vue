<template>
  <div class="container">
    <v-container>
      <v-row>
        <v-col cols="12">
          <v-card class="custom-card">
            <v-card-title class="fixed-header"><span style="margin-bottom: 5px;">我加入的群组</span></v-card-title>
            <v-card-subtitle class="custom-card-subtitle">
              <v-expansion-panels v-model="activePanel" class="custom-collapse">
                <v-expansion-panel
                  v-for="group in groupAdded"
                  :key="group.gid"
                  class="custom-collapse-item"
                >
                  <v-expansion-panel-header class="custom-collapse-item__header">
                    {{ group.group_name }}
                  </v-expansion-panel-header>
                  <v-expansion-panel-content class="custom-collapse-item__content">
                    <div class="description">{{ group.description }}</div>
                    <div class="password">密码: {{ group.password }}</div>
                  </v-expansion-panel-content>
                </v-expansion-panel>
              </v-expansion-panels>
            </v-card-subtitle>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      activePanel: [0],
      groupAdded: [
        {
          group_name: "计组学习小组",
          password: "password1",
          gid: "xxx1",
          description: "Description of group1"
        },
        {
          group_name: "今天我是大卷王",
          password: "password2",
          gid: "xxx2",
          description: "Description of group2"
        },
        {
          group_name: "前端学习小组",
          password: "password3",
          gid: "xxx3",
          description: "Description of group3"
        },
        {
          group_name: "后端学习小组",
          password: "password4",
          gid: "xxx4",
          description: "Description of group4"
        },
        {
          group_name: "后端学习小组",
          password: "password4",
          gid: "xxx5",
          description: "Description of group4"
        },
        {
          group_name: "后端学习小组",
          password: "password4",
          gid: "xxx6",
          description: "Description of group4"
        },
        {
          group_name: "后端学习小组",
          password: "password4",
          gid: "xxx7",
          description: "Description of group4"
        },
      ]
    };
  }
}
</script>

<style scoped>
.container {
  width: 100%;
  height: 45%
}

.fixed-header {
  background-color: #36a492;
  color: white;
  font-size: 18px;
  font-weight: bold;
  text-align: center;
}

.custom-card {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.custom-card-subtitle {
  padding: 7px;
  background: linear-gradient(135deg, #f3f4f7, #fff);
}

.custom-collapse {
  border: 1px solid #ccc;
  overflow-y: auto;
  max-height: 275px;
  background: #fafafa;
}

.custom-collapse-item {
  overflow: hidden;
  margin-bottom: 10px;
  background: none;
  transition: transform 0.3s, box-shadow 0.3s;
}

.custom-collapse-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.custom-collapse-item__header {
  background: linear-gradient(135deg, #57d59c, #36a492);
  color: #fff;
  border-radius: 8px 8px 0 0;
  padding: 10px;
}

.custom-collapse-item__header:hover {
  background: linear-gradient(135deg, #2c8e7d, #42b983);
}

.custom-collapse-item__content {
  border-radius: 0 0 8px 8px;
  padding: 10px;
  background: linear-gradient(135deg, #2c8e7d, #42b983);
}

.description {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 5px;
}

.password {
  font-size: 17px;
  font-weight: bold;
  color: #ff6f61;
}
</style>
