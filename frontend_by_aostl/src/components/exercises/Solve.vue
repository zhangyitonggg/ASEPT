<template>
    <div>
        66666<br/>
        {{content}}
    </div>
</template>

<script>
    export default{
        data() {
            return {
                content:'',
                id:-1,
            }
        },
        mounted() {
            this.id = this.$store.problemid;
            //this.getProblme(id);
        },
        methods: {
            getProblem(id) {
                //补充交互功能
            },
        }
    }
</script>