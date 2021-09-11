from mitmproxy.options import Options
from mitmproxy.proxy.config import ProxyConfig
from mitmproxy.proxy.server import ProxyServer
from mitmproxy.tools.dump import DumpMaster


import os
from get_json_data import get_data
from mitmproxy import ctx
from mitmproxy import http
from mitmproxy.addons import save

url_filter = 'shopee.ph/api/v4/search/search_items'
write_dir = os.path.dirname(os.path.realpath(__file__)) + '/MitmShopee'

class Shopeeitemscraper:
    def __init__(self):
        self.replay_response = None

    def response(self, flow: http.HTTPFlow): #write first 10 pages of the response
        if url_filter in flow.request.url:
            ctx.log.info(flow.request.url)
            page_num = round(int(flow.request.query['newest']) + int(flow.request.query['limit'])) / int(flow.request.query['limit'])
            starting_item = flow.request.query['newest'] #starting item number of page
            file_dir = write_dir + '/' + str(flow.request.query['keyword']) + '_' + str(page_num) + '.csv'
            if not os.path.exists(write_dir):
                os.makedirs(write_dir)
            response_df = get_data(flow.response.text, file_dir)
            if not response_df.empty: ctx.log.info("write success!")
            ctx.log.info('Page ' + str(page_num) + ' : ' + flow.request.url)

    def request(self, flow: http.HTTPFlow):
        if url_filter in flow.request.url:
            ctx.log.info(flow.request.url)       

if __name__ == "__main__":

    options = Options(listen_host='127.0.0.1', listen_port=8080, http2=True)
    m = DumpMaster(options, with_termlog=False, with_dumper=False)
    config = ProxyConfig(options)

    m.server = ProxyServer(config)
    m.addons.add(Shopeeitemscraper())

    try:
        print('starting mitmproxy')
        m.run()
    except KeyboardInterrupt:
        m.shutdown()