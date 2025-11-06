const { Component, mount, xml, useRef, onMounted, useState } = owl;

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
    const inputRef = useRef("add-input"); // Fetch a reference object (Ref from Owl) to a tag/element (denoted by t-ref)
    onMounted(() => inputRef.el.focus()); // Use inputRef.el to access the tag/element, then call focus() method
  }
  
  nextId = 1;
  tasks = useState([]);

  addTask(ev) {
    // 13 is keycode for ENTER
    if (ev.keyCode === 13) {
      const text = ev.target.value.trim();
      ev.target.value = "";
      if (text) {
          const newTask = {
              id: this.nextId++,
              text: text,
              isCompleted: false,
          };
          this.tasks.push(newTask);
      }
    }
  }
}

mount(Root, document.body);