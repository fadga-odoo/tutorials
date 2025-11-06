import { Orderline } from "@point_of_sale/app/components/orderline/orderline";
import { patch } from "@web/core/utils/patch";

patch(Orderline.prototype, {
    deleteLine(event) {
        event.stopPropagation();
        this.props.line.order_id.removeOrderline(this.props.line);
    }
})
