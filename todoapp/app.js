const { Component, mount, xml, useState } = owl;

class Task extends Component {
    static template = xml`
    <div class="task-container" t-att-class="props.tasky.isCompleted ? 'done' : ''">
        <input type="checkbox" t-att-checked="props.tasky.isCompleted"/>
        <span><t t-esc="props.tasky.text"/></span>
    </div>`;
    static props = ["tasky"]; // Used inside the tag: <Task taskItem="value">, meaning that we assign "value" to taskItem variable within the scope.
}

class Root extends Component {
  /**
   * t-foreach is used for looping: https://github.com/odoo/owl/blob/master/doc/reference/templates.md#loops* t-att is used for dynamic attribute: https://github.com/odoo/owl/blob/master/doc/reference/templates.md#dynamic-attributes
   * t-att is used for dynamic attribute: https://github.com/odoo/owl/blob/master/doc/reference/templates.md#dynamic-attributes
   * More about: https://github.com/odoo/owl/blob/master/doc/reference/templates.md#directives
   */
  static template = xml`
    <div class="task-list">
        <t t-foreach="tasks" t-as="taskItem" t-key="taskItem.id">
            <Task tasky="taskItem"/>
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