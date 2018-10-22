#include "output_settings.h"
#include "ui_output_settings.h"

output_settings::output_settings(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::output_settings)
{
    ui->setupUi(this);
}

output_settings::~output_settings()
{
    delete ui;
}
