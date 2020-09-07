from odoo import api, fields, models


class BomLotReports(models.TransientModel):
    _name = 'bom.lot.report'
    _description = 'Print Bom Lot Report'

    date_start = fields.Date(string='Start Date')
    date_end = fields.Date(string='End Date')

    def percentage_yield_report(self):

        # A truncation function obviously
        def truncate(n, decimals=0):
            multiplier = 10 ** decimals
            return int(n * multiplier) / multiplier

        # ---------------------------------OUTPUT--------------------------------------------
        # The output format
        mos = []
        size = {
            'us': {'mp/sup': 0, 'tr': 0, 'd2': 0, 'v': 0, 'vi': 0, 'd/rej': 0, 'total': 0, 'percentage': 0, 'initial': 9},
            'w': {'mp/sup': 0, 'tr': 0, 'd2': 0, 'v': 0, 'vi': 0, 'd/rej': 0, 'total': 0, 'percentage': 0, 'initial': 16},
            'bhl': {'mp/sup': 0, 'tr': 0, 'd2': 0, 'v': 0, 'vi': 0, 'd/rej': 0, 'total': 0, 'percentage': 0, 'initial': 23},
            'bhp': {'mp/sup': 0, 'tr': 0, 'd2': 0, 'v': 0, 'vi': 0, 'd/rej': 0, 'total': 0, 'percentage': 0, 'initial': 23},
            'rhl': {'mp/sup': 0, 'tr': 0, 'd2': 0, 'v': 0, 'vi': 0, 'd/rej': 0, 'total': 0, 'percentage': 0, 'initial': 30},
            'rhp': {'mp/sup': 0, 'tr': 0, 'd2': 0, 'v': 0, 'vi': 0, 'd/rej': 0, 'total': 0, 'percentage': 0, 'initial': 30},
            'yhl': {'mp/sup': 0, 'tr': 0, 'd2': 0, 'v': 0, 'vi': 0, 'd/rej': 0, 'total': 0, 'percentage': 0, 'initial': 38},
            'yhp': {'mp/sup': 0, 'tr': 0, 'd2': 0, 'v': 0, 'vi': 0, 'd/rej': 0, 'total': 0, 'percentage': 0, 'initial': 38},
            'stains': {'mp/sup': 0, 'tr': 0, 'd2': 0, 'v': 0, 'vi': 0, 'd/rej': 0, 'total': 0, 'percentage': 0, 'initial': 0},

        }
        for mo in self.env['mrp.production'].search([('date_planned_start', '>=', self.date_start), ('date_planned_start', '<=', self.date_end), ('state', 'in', ['done'])]).mapped('finished_move_line_ids'):

            # map lot_id's name to the output format initialized in size for records matching the mo
            for t in mo:
                for i in size:
                    for j in size[i]:
                        if t.lot_id:
                            if t.lot_id.name.lower().strip(' ') == f"{j}-{i}" or t.lot_id.name.lower().strip(' ') == f"{i}-{j}":
                                # size[i][j] += t.qty_done
                                size[i][j] += t.lot_id.no_of_pieces

        # calculate all line totals, exempting line total itself and percentage and initial.
        # calculate all column totals, returns a dictionary mapping column title to column total.
        # initialize initial total and the sum it up against hide initial total and its total output
        # create a dictionary mapping sum of each similar key in the size dict
        initial_total = 0
        seen = {}

        for i in size:
            for j in size[i]:
                if j != 'total' and j != 'percentage' and j != 'initial':
                    size[i]['total'] += size[i][j]

                if j != 'percentage' and j != 'initial':
                    if j in seen:
                        seen[j] += size[i][j]
                    else:
                        seen[j] = size[i][j]

            initial_total += (size[i]['total'] * size[i]['initial'])

        # calculate line percentage over all lines total
        for i in size:
            for j in size[i]:
                if size[i]['total'] == 0:
                    size[i]['percentage'] = 0
                else:
                    size[i]['percentage'] = truncate(
                        ((size[i]['total'] / seen['total']) * 100), 2)

        # calculate column percentage from column total / overall final total
        col_percentage = []

        for i in seen:
            percent = 0
            if seen['total'] == 0:
                percent = 0
            else:
                percent = truncate(((seen[i] / seen['total']) * 100), 2)

            col_percentage.append(percent)

        # ---------------------------------INPUT--------------------------------------------

        # search for the inputs in any children Mo's of an Mo and create values with it
        # initialize total_raw that calcualates the total consumed weight of all hides in the input
        # input total somes up the number of pieces in all inputs
        # transfer input is a list containing a dictionary of all inputs
        total_raw = 0
        input_total = 0
        transfer_input = []
        transfer_input_dict = {}

        for mo in self.env['mrp.production'].search([('date_planned_start', '>=', self.date_start), ('date_planned_start', '<=', self.date_end), ('state', 'in', ['done'])]):

            # for mo in self.env['mrp.production'].search(['|', ('id', '=', docids[0]), ('origin', '=', docs.name)]):
            for stock in self.env['stock.picking'].search([('origin', '=', mo.name)]):
                for line in stock.move_line_ids_without_package:

                    if line.product_id.isa_hide:
                        if product_id.id in transfer_input_dict:
                            transfer_input_dict[product_id.id]['pieces'] += line.product_id.x_studio_pieces_tot
                        else:
                            transfer_input_dict[product_id.id] = {
                                'product': line.product_id.product_template_attribute_value_ids[0].name if len(line.product_id.product_template_attribute_value_ids) > 0 else line.product_id.name,
                                'pieces': line.product_id.x_studio_pieces_tot,
                                'percentage': 0,
                            }

                        input_total += line.product_id.x_studio_pieces_tot

            for raw in mo.move_raw_ids:
                if raw.product_id.isa_hide:
                    total_raw += truncate(raw.quantity_done, 2)

        for key in transfer_input_dict:
            transfer_input.append(transfer_input_dict[key])

        for val in transfer_input_dict:
            if transfer_input_dict[val]['pieces'] == 0:
                transfer_input_dict[val]['percentage'] = 0
            else:
                transfer_input_dict[val]['percentage'] = truncate(
                    ((transfer_input_dict[val]['pieces'] / input_total) * 100), 2)

        data = {
            'mos': f"[ {', '.join(mos)} ]",
            'date_start': self.date_start.strftime('%d-%m-%Y'),
            'date_end': self.date_end.strftime('%d-%m-%Y'),
            'size': size,
            'transfer_input': transfer_input,
            'input_total': input_total,
            'col_total': seen,
            'total_raw': total_raw,
            'avg_per_pcs': truncate(total_raw/input_total, 2) if input_total > 0 else 0,
            'avg_yield': truncate(initial_total/total_raw, 2) if total_raw > 0 else 0,
            'initial_total': initial_total,
            'col_percentage': col_percentage,
        }
        return self.env.ref('bom_report.action_report_multiple_yields').report_action(self, data=data)
