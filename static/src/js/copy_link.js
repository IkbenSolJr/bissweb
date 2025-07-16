odoo.define('bissweb.CopyToClipboardWidget', function (require) {
    "use strict";

    const AbstractField = require('web.AbstractField');
    const fieldRegistry = require('web.field_registry');
    const CopyToClipboardWidget = AbstractField.extend({
        className: 'o_field_copy_to_clipboard',
        supportedFieldTypes: ['char', 'text'],
        _render: function () {
            this.$el.html(`
                <span class="copy-to-clipboard">${this.value || ''}</span>
                <button class="btn btn-secondary btn-sm copy-btn" title="Copy">
                    Copy Link
                </button>
            `);
            // Attach click event for copy functionality
            this.$el.find('.copy-btn').on('click', () => {
                navigator.clipboard.writeText(this.value || '');
                this.displayNotification({
                    title: "Đã copy link!",
                    message: `${this.value} đã được sao chép vào clipboard.`,
                    type: 'success',
                });
            });
        },
    });
    // Register the widget for reuse
    fieldRegistry.add('copy_to_clipboard', CopyToClipboardWidget);
    return CopyToClipboardWidget;
});
