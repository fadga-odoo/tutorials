const { Component, mount, xml, useState } = owl;

class Task extends Component {
    static template = xml`
    <div class="task-container" t-att-class="props.task.isCompleted ? 'done' : ''">
        <input type="checkbox" t-att-checked="props.task.isCompleted"/>
        <span><t t-esc="props.task.text"/></span>
    </div>`;
    static props = ["task"]; // Used inside the tag: <Task taskItem="value">, meaning that we assign "value" to taskItem variable within the scope (accessed by props.taskItem).
}

class Root extends Component {
  /**
   * t-foreach is used for looping: https://github.com/odoo/owl/blob/master/doc/reference/templates.md#loops* t-att is used for dynamic attribute: https://github.com/odoo/owl/blob/master/doc/reference/templates.md#dynamic-attributes
   * t-att is used for dynamic attribute: https://github.com/odoo/owl/blob/master/doc/reference/templates.md#dynamic-attributes
   * More about: https://github.com/odoo/owl/blob/master/doc/reference/templates.md#directives
   */
  static template = xml`
    <div class="task-list">
        <t t-foreach="tasks" t-as="task" t-key="task.id">
            <Task task="task"/>
        </t>
    </div>`;
  static components = { Task };
  
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
}

mount(Root, document.body);