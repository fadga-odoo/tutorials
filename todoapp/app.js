const { Component, mount, xml, useRef, onMounted } = owl;

class Task extends Component {
    static template = xml`
    <div class="task-container" t-att-class="props.task.isCompleted ? 'done' : ''">
        <input type="checkbox" t-att-checked="props.task.isCompleted"/>
        <span><t t-esc="props.task.text"/></span>
    </div>`;
    static props = ["task"]; // Used inside the tag: <Task taskItem="value">, meaning that we assign "value" to taskItem variable (property) within the scope (accessed by props.taskItem).
}

class Root extends Component {
  /**
   * t-foreach is used for looping: https://github.com/odoo/owl/blob/master/doc/reference/templates.md#loops* t-att is used for dynamic attribute: https://github.com/odoo/owl/blob/master/doc/reference/templates.md#dynamic-attributes
   * t-att is used for dynamic attribute: https://github.com/odoo/owl/blob/master/doc/reference/templates.md#dynamic-attributes
   * More about: https://github.com/odoo/owl/blob/master/doc/reference/templates.md#directives
   */
  static template = xml`
    <div class="todo-app">
      <input placeholder="Enter a new task" t-on-keyup="addTask" t-ref="add-input"/>
      <div class="task-list">
          <t t-foreach="tasks" t-as="task" t-key="task.id">
              <Task task="task"/>
          </t>
      </div>
    </div>`;
  static components = { Task };

  setup() {
    const inputRef = useRef("add-input");
    onMounted(() => inputRef.el.focus());
  }
  
  tasks = [
    {
      id: 1,
      text: "buy milk",
      isCompleted: true,
    },
    {
      id: 2,
      text: "clean house",
      isCompleted: false,
    }
  ];

  addTask(event) {
    if (event.keyCode === 13) {
      /**
       * This is how we fetch user input.
       * KeyboardEvent (event) will be sent to the browser and user input is stored in event.target.value.
       */
      const text = event.target.value.trim();
      event.target.value = "";
      console.log('adding task', text);
    }
  }
}

mount(Root, document.body);