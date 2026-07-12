import { Card, Typography } from "antd";


type PlaceholderPageProps = {
  title: string;
  module: string;
};

export function PlaceholderPage({ title, module }: PlaceholderPageProps) {
  return (
    <Card>
      <Typography.Title level={3}>{title}</Typography.Title>
      <Typography.Paragraph>{module}</Typography.Paragraph>
    </Card>
  );
}
