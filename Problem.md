# E - Shared Exercise Platform 共享训练平台

## Introduction 介绍

Please design a platform where students can upload and share questions. Students should be able to test themselves on it.

请设计一个可以让学生上传和分享问题的平台。学生们应该能够在平台上自测。

## Basic Requirements 基本要求

- Use GUI libraries such as Tkinter, PyQt5, or other front-end and back-end frameworks Python supported.
  使用诸如 Tkinter、PyQt 的 GUI 库或其他 Python 支持的前后端框架。
- The questions should include various formats such as multiple choice and fill in the blanks. Obtain questions on your own.
  平台上的问题问题应该包括多种形式，如多选和填空题。平台上的问题需要自行获取。
- The interface should be aesthetically pleasing but not overly fancy to distract from problem-solving. You can add additional features as desired, but they should be userfriendly and easy to use.
  平台界面应该美观但不过于花哨，以免分散你解决问题的重心。你可以根据需要添加其他功能，但它们应该是用户友好且易于使用的。

## Required Assignment 需要完成的需求

- Basic Requirements: User and administrator registration, login, and personal information management.
  基本要求：用户和管理员的注册、登录和个人信息的管理。
- User Groups: Users can choose to create and join groups, and users can search and join groups voluntarily.
  用户组：用户可以自主选择搜索、创建和加入团体。
- Upload: Recognize the text in PDF or pictures automatically. After recognition, the extracted text results can be edited to complete the input of questions. (Hint: Use OCR)
  上传：自动识别 PDF 和图片中的文本。识别后，可以对提取的文本结果进行编辑以输入问题。（提示：使用 OCR）
- Question Groups: Design your own or utilize existing data structures to organize questions into categories based on chapters or other criteria. When solving problems, users can choose a specific group of questions to work on. The problem-solving interface should be designed according to individual preferences without excessive requirements.
  问题分组：设计自己的或利用现有的数据结构，根据章节或其他标准将问题组织成类别。在解决问题时，用户可以选择一组特定的问题来处理。解决问题的界面没有过多要求，根据个人偏好进行设计即可。
- Question Sharing: Users can choose to share a group of questions with a specific group or make them available to everyone. The recipients of the shared questions gain access to the question group.
  分享问题：用户可以选择给一组特定的用户分享一组问题，或者将这组问题公开给所有人。被分享问题的用户可以访问这组问题。
- Search for Groups: The search should have customizable parameters, but the search scope should include shared question groups and the user's uploaded questions. It should not search for question groups that have not been shared.
  搜索问题组：搜索应具有可自定义的参数，但搜索范围应包括被分享给用户的问题组和用户自己上传的问题。搜索的范围不应该包括尚未被共享给该用户的问题组。
- Error log: Based on the user's incorrect answers, frequency of errors, and the user's specified subject and question quantity, consult relevant recommendation algorithms to generate a set of questions that the user should prioritize re-solving using a scientifically effective algorithm of your choice.
  错误日志：根据用户的错误答案、错误频率以及用户指定的主题和问题数量，查询相关的推荐算法，使用你选择的科学、有效的算法生成一组问题，用户应优先重新解决这些问题。

## Optional Assignment 可选的需求

- The system have the responsibility of screening sensitive words and removing them from the question bank. Find a way to implement this functionality.
  系统有责任筛选敏感词并将其从题库中删除。找到实现此功能的方法。
- Visualize student abilities. Based on the type and time of incorrect answers, refer to relevant materials and define a conversion standard from student's incorrect question information to student's ability information. Create a graph showing the change in student abilities over time.
  将学生的能力形象化。根据错误答案的类型和时间，参考相关材料，定义学生错误问题信息到学生能力信息的转换标准。创建一个图表，显示学生能力随时间的变化。
- Implement additional features as desired, earning extra points based on practicality and workload.
  根据需要实现其他功能，根据实用性和工作量获得加分。