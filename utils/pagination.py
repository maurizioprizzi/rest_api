class Pagination:
    def __init__(self, data, page, per_page):
        self.data = data
        self.page = page
        self.per_page = per_page

    def paginate(self):
        total_items = len(self.data)
        total_pages = (total_items + self.per_page - 1) // self.per_page

        start_index = (self.page - 1) * self.per_page
        end_index = start_index + self.per_page

        paginated_data = self.data[start_index:end_index]

        meta = {
            'page': self.page,
            'total_pages': total_pages,
            'total_items': total_items
        }

        return {
            'data': paginated_data,
            'meta': meta
        }
