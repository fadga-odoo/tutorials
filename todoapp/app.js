const { Component, mount, xml } = owl;

class Root extends Component {
/**
 * t-foreach is used for looping: https://github.com/odoo/owl/blob/master/doc/reference/templates.md#loops
 * t-att is used for dynamic attribute: https://github.com/odoo/owl/blob/master/doc/reference/templates.md#dynamic-attributes
 * More about: https://github.com/odoo/owl/blob/master/doc/reference/templates.md#directives
 */
  static template = xml`
    <div class="task-list">
        <t t-foreach="tasks" t-as="task" t-key="task.id">
            <div class="task" t-att-class="task.isCompleted ? 'done' : ''">
                <input type="checkbox" t-att-checked="task.isCompleted"/>
                <span><t t-esc="task.text"/></span>
            </div>
        </t>
    </div>`;

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
    },
  ];
}

mount(Root, document.body);