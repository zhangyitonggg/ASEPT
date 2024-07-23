const base = {
    baseUrl: 'http://localhost:8000',
    login: '/security/token',
    logon: '/create_user',
    news_getannouncements: '/news/get_announcements?max_announcements=20',
    showJoinedGroups: '/user_group/show_joined_groups',
    leaveGroup: '/user_group/leave_group',
    showCreatedGroups: '/user_group/show_create_groups',
    createGroup: '/user_group/create_group',
    modifyGroup: '/user_group/modify_group',
    showUnGroups: '/user_group/show_unentered_groups',
    createProblem: '/problems/upload_problem',
<<<<<<< HEAD
    createProblemGroup: '/problems/create_problem_group',
    change_problem_group_info: '/problems/change_problem_group_info',
    add_problem_to_group: '/problems/add_problem_to_group',
    share_problem_group_to_user_group: '/problems/share_problem_group_to_user_group',
    add_problem_tag: '/problems/add_problem_tag',
    search_problem_by_tag: '/problems/search_problem_by_tag',
    get_my_problems: '/problems/get_my_problems',
    submit_problem: '/problems/submit_problem',
    get_user_statistics: '/problems/get_user_statistics',
    get_problem_recommend: '/problems/get_problem_recommend',
    get_problem: '/problems/get_problem',
=======
    joinGroup: '/user_group/join_group',
>>>>>>> b86a0db9a4dbeb85ad41d7ad96173c4beb4f4526
}

export default base;